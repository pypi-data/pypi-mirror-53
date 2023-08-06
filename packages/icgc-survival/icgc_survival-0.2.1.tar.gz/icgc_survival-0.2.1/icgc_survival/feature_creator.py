import pandas as pd


def extract_chromosome_counts(ssm_or_cnsm_df):
    if "icgc_mutation_id" in ssm_or_cnsm_df.columns:
        ssm_or_cnsm_df = ssm_or_cnsm_df[["icgc_donor_id", "icgc_mutation_id", "chromosome"]]
        ssm_or_cnsm_df = ssm_or_cnsm_df.drop_duplicates()
    else:
        ssm_or_cnsm_df = ssm_or_cnsm_df[["icgc_donor_id", "chromosome"]].reset_index()
    ssm_or_cnsm_df = ssm_or_cnsm_df.groupby(["icgc_donor_id", "chromosome"]).count().reset_index()
    donors = ssm_or_cnsm_df["icgc_donor_id"].unique()
    chromosomes = ssm_or_cnsm_df["chromosome"].unique()
    if "icgc_mutation_id" in ssm_or_cnsm_df.columns:
        helper_list = [list(a) for a in zip(ssm_or_cnsm_df["icgc_donor_id"], ssm_or_cnsm_df["chromosome"],
                       ssm_or_cnsm_df["icgc_mutation_id"])]
    else:
        helper_list = [list(a) for a in zip(ssm_or_cnsm_df["icgc_donor_id"], ssm_or_cnsm_df["chromosome"],
                                            ssm_or_cnsm_df["index"])]
    feature_df = pd.DataFrame(0, index=donors, columns=chromosomes, dtype="int16")
    for cn in helper_list:
        feature_df.at[cn[0], cn[1]] = cn[2]

    return feature_df


def extract_gene_affected_counts(ssm_df):
    ssm_df = ssm_df[["icgc_donor_id", "icgc_mutation_id", "gene_affected"]]
    ssm_df = ssm_df.drop_duplicates()
    ssm_df = ssm_df.groupby(["icgc_donor_id", "gene_affected"]).count().reset_index()
    donors = ssm_df["icgc_donor_id"].unique()
    genes = ssm_df["gene_affected"].unique()
    helper_list = [list(a) for a in zip(ssm_df["icgc_donor_id"], ssm_df["gene_affected"], ssm_df["icgc_mutation_id"])]
    feature_df = pd.DataFrame(0, index=donors, columns=genes, dtype="int16")
    for mut in helper_list:
        feature_df.at[mut[0], mut[1]] = mut[2]

    return feature_df


def extract_expression_features(expr_df, gene_model, type):
    expr_df = expr_df[["icgc_donor_id", "gene_model", "gene_id", type]]
    expr_df = expr_df[expr_df["gene_model"] == gene_model]
    expr_df = expr_df.drop("gene_model", axis=1)
    expr_df[type] = expr_df[type].astype("float16")
    expr_df = expr_df.drop_duplicates()

    print(expr_df.shape)

    donors = expr_df["icgc_donor_id"].unique()
    genes = expr_df["gene_id"].unique()
    helper_list = [list(a) for a in
                   zip(expr_df["icgc_donor_id"], expr_df["gene_id"], expr_df[type])]
    feature_df = pd.DataFrame(0, index=donors, columns=genes, dtype="float16")
    for expr in helper_list:
        feature_df.at[expr[0], expr[1]] = expr[2]

    return feature_df




