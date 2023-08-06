# -*- coding: utf-8 -*-

"""Console script for shiptv."""
import sys
import logging

import click
import pandas as pd

from shiptv.shiptv import genbank_metadata, add_user_metadata, parse_tree, \
    write_html_tree, parse_leaf_list, prune_tree, reorder_metadata_fields, \
    get_metadata_fields, highlight_user_samples, try_fix_serotype_metadata, \
    try_fix_country_metadata, \
    try_fix_collection_date_metadata, try_fix_host_metadata, collapse_branches


@click.command()
@click.option('-r', '--ref-genomes-genbank',
              required=False,
              type=click.Path(exists=True, dir_okay=False),
              help='Reference genome sequences Genbank file')
@click.option('-n', '--newick',
              required=True, type=click.Path(exists=True, dir_okay=False),
              help='Phylogenetic tree Newick file')
@click.option('-N', '--output-newick',
              type=click.Path(),
              help='Output Newick file')
@click.option('-o', '--output-html', type=click.Path(),
              required=True, help='Output HTML tree path')
@click.option('-m', '--output-metadata-table',
              type=click.Path(),
              required=True, help='Output metadata table path')
@click.option('--leaflist',
              required=False,
              type=click.Path(),
              default=None,
              help='Optional leaf names to select from phylogenetic tree for '
                   'pruned tree visualization. One leaf name per line.')
@click.option('--genbank-metadata-fields',
              required=False,
              type=click.Path(),
              default=None,
              help='Optional fields to extract from Genbank source metadata. '
                   'One field per line.')
@click.option('--user-sample-metadata',
              required=False,
              type=click.Path(),
              default=None,
              help='Optional tab-delimited metadata for user samples to join '
                   'with metadata derived from reference genome sequences '
                   'Genbank file. Sample IDs must be in the first column.')
@click.option('--metadata-fields-in-order',
              required=False,
              type=click.Path(),
              default=None,
              help='Optional list of fields in order to output in metadata '
                   'table and HTML tree visualization. One field per line.')
@click.option('--dont-fix-metadata', is_flag=True,
              help='Do not automatically fix metadata (only on Genbank file metadata)')
@click.option('-C', '--collapse-support', default=-1, type=float,
              help='Collapse internal branches below specified bootstrap '
                   'support value (default -1 for no collapsing)')
def main(ref_genomes_genbank,
         newick,
         output_newick,
         output_html,
         output_metadata_table,
         leaflist,
         genbank_metadata_fields,
         user_sample_metadata,
         metadata_fields_in_order,
         dont_fix_metadata,
         collapse_support):
    """Create HTML tree visualization with metadata.

    The metadata for reference genomes can be extracted from the specified
    Genbank file.

    Any leaf names that are present in the tree but not present in the Genbank
    file are assumed to be user samples and are flagged as such in the
    metadata table as "user_sample"="Yes".
    """
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s '
                               '[in %(filename)s:%(lineno)d]',
                        level=logging.INFO)
    tree = parse_tree(newick)
    if collapse_support != -1:
        logging.info(f'Collapsing internal branches with support values less '
                     f'than {collapse_support}')
        collapse_branches(tree, collapse_support)
    if output_newick:
        tree.write(outfile=output_newick)
    if ref_genomes_genbank:
        df_metadata = genbank_metadata(ref_genomes_genbank)
        logging.info(f'Parsed metadata from "{ref_genomes_genbank}" with columns '
                     f'"{";".join(df_metadata.columns)}')
        if dont_fix_metadata:
            logging.warning('Not fixing any genome metadata.')
        else:
            try_fix_serotype_metadata(df_metadata)
            try_fix_country_metadata(df_metadata)
            try_fix_collection_date_metadata(df_metadata)
            try_fix_host_metadata(df_metadata)
        metadata_fields = get_metadata_fields(genbank_metadata_fields)
        # only use columns present in the reference genome metadata
        metadata_fields = [x for x in metadata_fields if
                           x in list(df_metadata.columns)]
        logging.info(f'Metadata table fields: {";".join(metadata_fields)}')
        
    else:
        df_metadata = pd.DataFrame(index=tree.get_leaf_names())
        metadata_fields = []
    df_metadata = highlight_user_samples(df_metadata, metadata_fields,
                                         tree.get_leaf_names())
    
    df_metadata = prune_tree(df_metadata, parse_leaf_list(leaflist), tree)
    if user_sample_metadata:
        add_user_metadata(df_metadata, user_sample_metadata)
    df_metadata = reorder_metadata_fields(df_metadata, metadata_fields_in_order)
    df_metadata.to_csv(output_metadata_table, sep='\t')
    logging.info(f'Wrote tab-delimited genome metadata table with '
                 f'{df_metadata.shape[0]} rows and '
                 f'{df_metadata.shape[1]} columns to '
                 f'"{output_metadata_table}"')
    write_html_tree(df_metadata, output_html, tree)
    logging.info(f'Wrote HTML tree to "{output_html}"')


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
