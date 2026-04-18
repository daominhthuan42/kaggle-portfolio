# stats_utils.py
import logging
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scikit_posthocs as sp
import pingouin as pg
from IPython.display import display, HTML
from utils.colors_utils import ColorUtils
from scipy.stats import chi2_contingency, kruskal, levene, ttest_ind, mannwhitneyu
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import skew, kurtosis, probplot

class StatUtils:
    """
    Utility class for common statistical tests and analysis.
    """

    @staticmethod
    def cal_ChiSquare(cat_feature: str, target_feature: str, df: pd.DataFrame, logger: logging.Logger,
                  show_expected: bool=False, show_residuals: bool=False) -> None:
        """
        Perform a Chi-Square test of independence to evaluate whether two categorical variables
        are statistically associated (i.e., dependent) or independent from each other.

        This function tests the null hypothesis that the two categorical variables are independent.
        It prints the test statistic, degrees of freedom, p-value, and an interpretation based on the p-value.
        Optionally, it displays the expected frequency table under independence, and standardized residuals
        (including a heatmap) which help to identify specific group-level deviations.

        Parameters
        ----------
        cat_feature : str
            Name of the first categorical variable (typically the feature).

        target_feature : str
            Name of the second categorical variable (typically the target label).

        df : pd.DataFrame
            The input DataFrame containing the data.

        show_expected : bool, default=False
            If True, prints the expected frequencies under the assumption of independence.

        show_residuals : bool, default=False
            If True, prints the standardized residuals and shows them as a heatmap
            to identify where the strongest associations/deviations occur.

        logger : logging.Logger
            Logger instance used to record the analysis process, statistical results,
            and decision messages.

        Returns
        -------
        None
            Prints the Chi-Square test result, including statistical significance interpretation.
            Optionally prints expected values and standardized residuals.

        Notes
        -----
        - Hypotheses:
            H₀ (Null):     The two variables are independent (no association).
            H₁ (Alt.):      There is a dependency or association between the variables.

        - Interpretation:
            If p-value < 0.05 → Reject H₀ → Conclude that the variables are significantly associated.
            If p-value ≥ 0.05 → Fail to reject H₀ → No statistically significant association found.

        - Standardized residuals:
            - Values > +2 or < -2 indicate strong deviation from expected frequency (local dependency).
            - Useful for identifying specific group-level contributions to the overall Chi-Square result.

        References
        ----------
        - https://en.wikipedia.org/wiki/Chi-squared_test
        - https://www.scribbr.com/statistics/chi-square-test-of-independence/
        """

        logger.info(f"Chi-Square Test of Independence: '{cat_feature}' vs. '{target_feature}'...")

        # Contingency table
        crosstab = pd.crosstab(df[cat_feature], df[target_feature])
        chi2, p, dof, expected = chi2_contingency(crosstab)

        logger.info(f"Chi-squared statistic: {chi2:.3f}")
        logger.info(f"Degrees of freedom: {dof}")
        logger.info(f"p-value: {p:.6f}")

        if p < 0.05:
            logger.info("Result: p-value < 0.05 → Reject H₀")
            logger.info(f"Variables '{cat_feature}' and '{target_feature}' are statistically associated.")

            # Optional: show standardized residuals
            if show_residuals:
                residuals = (crosstab - expected) / np.sqrt(expected)
                logger.debug("Displaying standardized residuals heatmap.")
                # Heatmap of residuals
                plt.figure(figsize=(10, 7))
                sns.heatmap(residuals, annot=True, cmap=sns.diverging_palette(0, 230, 90, 60, as_cmap=True), center=0, fmt=".2f", linewidths=0.5)
                plt.title(f"Standardized Residuals Heatmap: {cat_feature} vs {target_feature}", weight="bold", fontsize=12, pad=15)
                plt.ylabel(cat_feature)
                plt.xlabel("")
                plt.tight_layout()
                plt.show()
        else:
            logger.warning("Result: p-value ≥ 0.05 → Fail to reject H0")
            logger.warning(f"No statistically significant association detected between '{cat_feature}' and '{target_feature}'.")

        # Optional: show expected frequencies
        if show_expected:
            logger.debug("Expected frequencies under independence assumption:")
            print(pd.DataFrame(expected, index=crosstab.index, columns=crosstab.columns))

    @staticmethod
    def perform_kruskal_test(df: pd.DataFrame, categorical_feature: str,
                            numeric_feature: str, logger: logging.Logger) -> None:
        """
        Perform the Kruskal-Wallis H-test to determine whether there are statistically
        significant differences in the distribution of a numeric variable across
        three or more independent groups.

        If the result is significant (p < 0.05), Dunn's post-hoc test with Bonferroni correction
        is performed to identify which group pairs differ.

        Parameters
        ----------
        df : pd.DataFrame
            The input dataset containing the categorical and numerical variables.

        categorical_feature : str
            The name of the categorical feature that defines the groups.

        numeric_feature : str
            The name of the numeric feature to be compared across groups.

        logger : logging.Logger
            Logger instance used to record the analysis process, statistical results,
            and decision messages.

        Returns
        -------
        None
            Prints the Kruskal-Wallis H-statistic, p-value, interpretation, and
            optionally the results of Dunn's post-hoc test.

        Notes
        -----
        - H₀ (null hypothesis): The distribution of the numeric variable is the same across all groups.
        - H₁ (alternative hypothesis): At least one group has a different distribution.
        - If p < 0.05 → reject H₀ → use Dunn’s test to explore specific group differences.
        - Kruskal-Wallis is a non-parametric alternative to one-way ANOVA.
        - It does not assume normality, but assumes:
            1. Independent samples
            2. Ordinal or continuous response variable
            3. Similar shapes of distributions

        Requirements
        ------------
        - `scipy.stats.kruskal`
        - `scikit-posthocs` package for Dunn’s test (`import scikit_posthocs as sp`)

        References
        ----------
        - https://www.geeksforgeeks.org/kruskal-wallis-test/
        - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html
        - https://scikit-posthocs.readthedocs.io/en/latest/index.html
        """

        # Extract values
        groups = df[categorical_feature].dropna().unique()
        if len(groups) < 3:
            logger.error(f"Error: Kruskal-Wallis H-test requires 3 or more groups.")
            return
        else:
            logger.info(f"Kruskal-Wallis Test: {numeric_feature} ~ {categorical_feature}...")
            logger.debug(f"Number of groups detected: {len(groups)}")
            data_groups = [df[df[categorical_feature] == g][numeric_feature].dropna() for g in groups]

            # Perform kruskal
            stat, p = kruskal(*data_groups)

            logger.info(f"Kruskal-Wallis H-statistic: {stat:.3f}")
            logger.info(f"p-value: {p}")

            if p < 0.05:
                logger.info("Significant difference detected among groups (p < 0.05).")
                logger.debug("Running Dunn's Post-Hoc Test (Bonferroni corrected)...")
                dunn_result = sp.posthoc_dunn(df, val_col=numeric_feature, group_col=categorical_feature, p_adjust="bonferroni")
                print(dunn_result)
            else:
                logger.warning("No statistically significant difference detected between groups (p ≥ 0.05).")

    @staticmethod
    def check_normality_with_plots(df: pd.DataFrame, logger: logging.Logger, feature: str, target_feature: str, 
                                   threshold_skew_1: float=0.5, threshold_skew_2: float=1.0,
                                   threshold_kurt: float=1.5, ncols: int=2) -> bool:
        """
        Assess the normality of a numerical feature across groups of a categorical variable
        using skewness, kurtosis, and Q–Q plot visualization.

        This function evaluates whether the distribution of a specified numerical feature
        follows an approximately normal distribution within each category of a target
        grouping variable. The assessment is based on:

        - Skewness (symmetry of the distribution)
        - Kurtosis (tailedness of the distribution)
        - Visual inspection using Q–Q plots

        If at least one group violates the normality assumption, the function flags
        non-normality and recommends the use of non-parametric statistical tests
        (e.g., Kruskal–Wallis, Mann–Whitney U).

        The function also produces:
        - Group-wise summary statistics (skewness, kurtosis, remarks)
        - Q–Q plots for visual assessment
        - A styled results table for reporting

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataset containing both numerical and categorical variables.

        logger : logging.Logger, optional
            Logger instance used for tracking analysis steps, statistical results,
            and recommendations.

        feature : str
            Name of the numerical feature to be tested for normality.

        target_feature : str
            Name of the categorical variable used to define comparison groups.

        threshold_skew_1 : float, default=0.5
            Threshold for approximate symmetry (|skewness| ≤ threshold_skew_1).

        threshold_skew_2 : float, default=1.0
            Threshold for moderate skewness
            (threshold_skew_1 < |skewness| ≤ threshold_skew_2).

        threshold_kurt : float, default=1.5
            Absolute kurtosis threshold for approximate normality.

        ncols : int, default=2
            Number of Q–Q plots displayed per row.

        Returns
        -------
        bool
            True if at least one group violates the normality assumption.
            False if all groups are approximately normally distributed.

        Notes
        -----
        - This function is intended for exploratory data analysis and
        assumption checking prior to statistical hypothesis testing.
        - For small sample sizes, normality assessment should be interpreted
        with caution.
        - When non-normality is detected, non-parametric tests are preferred.

        Examples
        --------
        >>> check_normality_with_plots(
        ...     df=data,
        ...     feature="st_depression",
        ...     target_feature="heart_disease"
        ... )
        """

        results = []
        non_normal_detected = False

        logger.info(f"Checking normality of feature '{feature}' by groups of '{target_feature}'...")

        # ===== Group evaluation =====
        logger.info("Evaluating distribution characteristics (skewness & kurtosis)...")

        groups = df[target_feature].dropna().unique()
        logger.debug(f"Number of groups detected: {len(groups)}")
        logger.debug(f"Thresholds → |skew|≤{threshold_skew_1}, |kurtosis|≤{threshold_kurt}")

        for grp, subset in df.groupby(target_feature):
            data = subset[feature].dropna()
            sk = skew(data)
            kt = kurtosis(data)
            abs_sk = abs(sk)
            abs_kt = abs(kt)

            # Skewness interpretation
            if abs_sk <= threshold_skew_1:
                skew_remark = "Approximately symmetric"
            elif abs_sk <= threshold_skew_2:
                skew_remark = "Moderately skewed"
            else:
                skew_remark = "Highly skewed"

            # Kurtosis interpretation
            if abs_kt < threshold_kurt:
                kurt_remark = "Normal tails"
            else:
                kurt_remark = "Heavy/light tails"

            remark = f"{skew_remark}, {kurt_remark}"
            results.append({
                "Feature": feature,
                "Group": grp,
                "Skewness": f"{sk:.4f}",
                "Kurtosis": f"{kt:.4f}",
                "Remark": remark
            })

            logger.debug(f"[{target_feature}={grp}] skew={sk:.4f}, kurtosis={kt:.4f} → {remark}")

            # Flag if any group is not approximately normal
            if not (abs_sk <= threshold_skew_1 and abs_kt <= threshold_kurt):
                non_normal_detected = True

        # === Visual Q–Q plots ===
        logger.info("Generating Q–Q plots for visual assessment...")

        n_groups = df[target_feature].nunique()
        nrows = int(np.ceil(n_groups / ncols))
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(6 * ncols, 4.5 * nrows))
        axes = np.array(axes).reshape(-1)

        for i, grp in enumerate(df[target_feature].unique()):
            ax = axes[i]
            data = df.loc[df[target_feature] == grp, feature].dropna()
            probplot(data, dist="norm", plot=ax)
            ax.set_title(f"{feature} — {grp}", fontsize=12, weight="bold")
            ax.grid(alpha=0.3)

        for j in range(i + 1, len(axes)):
            axes[j].axis("off")

        plt.suptitle(f"Q–Q Plots of {feature} by {target_feature}", fontsize=12, weight="bold", y=1.02)
        plt.tight_layout()
        plt.show()

        # === Display results table ===
        df_result = pd.DataFrame(results)
        cm = sns.light_palette("blue", as_cmap=True)
        styled = (
            df_result.style
            .background_gradient(subset=["Skewness"], cmap=cm, vmin=-1, vmax=1)
            .background_gradient(subset=["Kurtosis"], cmap=cm, vmin=-1.5, vmax=1.5)
            .set_caption(
                f'<b><span style="font-size:14px; text-align:center; display:block;">'
                f'Skewness & Kurtosis of {feature} by {target_feature}'
                f'</span></b>'
            )
            .set_table_attributes('style="width:80%; margin:auto;"')
        )
        display(styled)

        # === Final evaluation ===
        if non_normal_detected:
            logger.warning("Normality assumption violated in at least one group.")
            logger.info("Recommendation: Use non-parametric tests (Kruskal–Wallis / Mann–Whitney U).")
        else:
            logger.info("All groups approximately follow a normal distribution.")

        return non_normal_detected

    @staticmethod
    def perform_anova_with_tukey(df: pd.DataFrame, logger: logging.Logger, numeric_feature: str, 
                                 categorical_feature: str, typ: int=2) -> None:
        """
        Perform a One-Way ANOVA test to determine whether there are statistically
        significant differences between the means of three or more independent groups.

        If the ANOVA test is significant (p < 0.05), Tukey's HSD post-hoc test is performed
        to identify which specific pairs of groups differ from each other.

        Parameters
        ----------
        df : pd.DataFrame
            The input dataset containing the numeric and categorical features.

        logger : logging.Logger
            Logger instance used to record the analysis process, statistical results,
            and decision messages.

        numeric_feature : str
            The name of the numerical (continuous) response variable.

        categorical_feature : str
            The name of the categorical (independent) variable used to group the data.

        typ : int, optional (default=2)
            The type of sum of squares to use in the ANOVA test:
            - Type I (1): Sequential.
            - Type II (2): Default and commonly used for balanced designs.
            - Type III (3): Use when model includes interaction terms or unbalanced data.

        Returns
        -------
        None
            Prints the ANOVA table, p-value, interpretation, and (if significant) the Tukey HSD test summary.

        Notes
        -----
        - H₀ (null hypothesis): All group means are equal.
        - H₁ (alternative hypothesis): At least one group mean is different.
        - If p < 0.05 → reject H₀ → perform Tukey’s HSD to find which groups differ.
        - Assumptions:
            1. Independence of observations
            2. Normally distributed groups (Shapiro or Anderson test can check this)
            3. Homogeneity of variances (Levene's test)

        References
        ----------
        - https://www.scribbr.com/statistics/one-way-anova/
        - https://en.wikipedia.org/wiki/Analysis_of_variance
        - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.tukey_hsd.html
        """

        # Extract unique groups
        groups = df[categorical_feature].dropna().unique()

        if len(groups) < 3:
            logger.error("Error: ANOVA requires at least 3 groups.")
            return
        else:
            logger.info(f"Running ANOVA Test: {numeric_feature} ~ {categorical_feature} (Type {typ})...")
            logger.debug(f"Number of groups detected: {len(groups)}")
            # Fit OLS model
            model = ols(f"{numeric_feature} ~ C({categorical_feature})", data=df).fit()

            # Perform ANOVA
            anova_table = anova_lm(model, typ=typ)
            logger.debug("ANOVA Table:")
            print(anova_table)

            # Extract p-value
            p_value = anova_table["PR(>F)"].iloc[0]

            if p_value < 0.05:
                logger.info("Result: p-value < 0.05 → Reject H0")
                logger.info("Conclusion: Significant difference exists between group means.")

                # ===== Post-hoc Tukey =====
                logger.debug("Running Tukey's HSD post-hoc test...")

                tukey = pairwise_tukeyhsd(df[numeric_feature], df[categorical_feature])
                print(tukey.summary())
            else:
                logger.warning("Result: p-value ≥ 0.05 → Fail to reject H0")
                logger.warning("Conclusion: No statistically significant difference between group means.")

    @staticmethod
    def perform_welch_anova(df: pd.DataFrame, logger: logging.Logger, numeric_feature: str,
                            categorical_feature: str) -> None:
        """
        Perform Welch’s ANOVA test to compare group means when the assumption of equal variances
        is violated but normality approximately holds.

        This version of ANOVA adjusts for unequal variances and sample sizes across groups.
        If the Welch’s ANOVA is significant (p < 0.05), a Games–Howell post-hoc test is performed
        to identify which specific group pairs differ significantly.

        Parameters
        ----------
        df : pd.DataFrame
            The input dataset containing both numeric and categorical variables.

        logger : logging.Logger
            Logger instance used to record the analysis process, statistical results,
            and decision messages.

        numeric_feature : str
            The name of the continuous (dependent) variable.

        categorical_feature : str
            The name of the categorical (independent) variable representing group membership.

        Returns
        -------
        None
            Prints Welch’s ANOVA summary, p-value interpretation, and Games–Howell post-hoc results.

        Notes
        -----
        - H₀ (null hypothesis): All group means are equal.
        - H₁ (alternative hypothesis): At least one group mean differs.
        - If p < 0.05 → reject H₀ → perform Games–Howell test.
        - Assumptions:
            1. Groups are independent.
            2. Data within each group are approximately normal.
            3. Variances are not necessarily equal (heteroscedasticity allowed).

        Key Differences vs Classical ANOVA
        ----------------------------------
        - Welch’s ANOVA does **not assume equal variances**.
        - More robust when sample sizes and variances differ across groups.
        - Use **Games–Howell post-hoc test** instead of Tukey HSD.

        References
        ----------
        - Welch, B. L. (1951). "On the comparison of several mean values: an alternative approach."
        Biometrika, 38(3/4), 330–336.
        - Games, P. A., & Howell, J. F. (1976). "Pairwise multiple comparison procedures with unequal N’s and/or variances."
        Journal of Educational Statistics, 1(2), 113–125.
        """

        # Drop NaN rows
        df = df[[numeric_feature, categorical_feature]].dropna()

        # Extract group values
        groups = [df.loc[df[categorical_feature] == g, numeric_feature] for g in df[categorical_feature].unique()]

        if len(groups) < 3:
            logger.error("Error: Welch’s ANOVA requires 3 or more groups.")
            return

        logger.info(f"Running Welch’s ANOVA Test: {numeric_feature} ~ {categorical_feature}")
        logger.debug(f"Number of groups detected: {len(groups)}")
        logger.info("Assessing mean differences under heteroscedastic conditions...")

        # ===== Welch ANOVA (Pingouin) =====
        welch_table = pg.welch_anova(
            dv=numeric_feature,
            between=categorical_feature,
            data=df
        )

        # Extract p-value
        p_value = welch_table["p-unc"].iloc[0]
        f_stat = welch_table["F"].iloc[0]

        logger.info(f"Welch ANOVA F-statistic: {f_stat:.4f}")
        logger.info(f"p-value: {p_value:.6f}")

        # Diagnostic output
        logger.debug("Welch ANOVA table:")
        print(welch_table)

        # ===== Decision =====
        if p_value < 0.05:
            logger.info("Result: p-value < 0.05 → Reject H0")
            logger.info("Conclusion: Significant mean differences detected.")

            # ===== Games–Howell post-hoc =====
            logger.debug("Running Games–Howell post-hoc test...")
            gh_result = pg.pairwise_gameshowell(dv=numeric_feature, between=categorical_feature, data=df)

            display(gh_result.style.background_gradient(cmap=sns.light_palette("blue", as_cmap=True)) \
                    .format(precision=4).set_table_attributes('style="width:80%; margin:auto;"'))
        else:
            logger.warning("Result: p-value ≥ 0.05 → Fail to reject H0")
            logger.warning("Conclusion: No statistically significant mean differences detected.")

    @staticmethod
    def check_homogeneity_of_variance(df: pd.DataFrame, logger: logging.Logger, feature: str, target_feature: str, 
                                      alpha: float=0.05, ratio_threshold: float=2.0) -> dict:
        """
        Check homogeneity of variances across groups using Levene’s test (median-centered).
        Also computes variance ratios and provides practical interpretation.

        ---
        Parameters
        ----------
        df : pd.DataFrame
            Input dataset containing numeric and categorical features.

        logger : logging.Logger
            Logger instance used to record the analysis process, statistical results,
            and decision messages.

        feature : str
            Numeric variable to test.

        target_feature : str
            Categorical grouping variable.

        alpha : float, default = 0.05
            Significance level for hypothesis testing.

        ratio_threshold : float, default = 2.0
            Threshold for maximum acceptable variance ratio (max(var)/min(var)).
            If ratio > threshold → indicates heteroscedasticity in practice.

        ---
        Returns
        -------
        dict
            Dictionary with test statistic, p-value, variance ratio, and recommendation.

        ---
        Interpretation Logic
        ---------------------
        Step 1: Statistical Test
            - H₀: All group variances are equal.
            - H₁: At least one group has a different variance.
            - Levene’s Test (center='median') is robust to non-normality.

        Step 2: Practical Variance Ratio
            - ratio = max(var_i) / min(var_i)
            - < 2 → practically equal
            - 2–4 → moderate difference
            - > 4 → strong heterogeneity

        Step 3: Recommendation
            - If p > 0.05 AND ratio < 2 → Use One-Way ANOVA or Independent Two-Sample T-Test
            - If p < 0.05 BUT ratio < 2 → Statistical diff, but practically negligible → ANOVA or T-Test are acceptable, but Welch’s ANOVA or Welch’s T-Test is recommended.
            - If ratio ≥ 2 OR p < 0.05  →  Use Kruskal–Wallis or Mann–Whitney U test.
        """

        # Group data by category
        groups = [df.loc[df[target_feature] == g, feature].dropna() for g in df[target_feature].unique()]
        logger.info("Check homogeneity of variances across groups using Levene’s test (median-centered)")
        logger.debug(f"Number of groups detected: {len(groups)}")

        if len(groups) < 2:
            logger.error("Levene’s test requires at least 2 groups.")
            return False, False

        # Perform Levene’s Test (robust version)
        stat, p = levene(*groups, center="median")

        # Compute variance ratio (max/min)
        variances = [np.var(g, ddof=1) for g in groups]
        ratio = max(variances) / min(variances)
        anova_use = False
        is_homogeneous_variances = False
        # Determine interpretation
        if p > alpha and ratio < ratio_threshold:
            status = "Variances are statistically and practically homogeneous."
            recommendation = "Use One-Way ANOVA or Independent Two-Sample T-Test."
            is_homogeneous_variances = True
            anova_use = True
        elif p < alpha and ratio < ratio_threshold:
            status = "Statistically different variances, but practical difference is small."
            recommendation = "ANOVA or T-Test are acceptable, but Welch’s ANOVA or Welch’s T-Test is recommended."
            anova_use = True
        else:
            status = "Strong variance heterogeneity detected."
            recommendation = "Use Kruskal–Wallis or Mann–Whitney U test."

        # Display summary table
        summary_df = pd.DataFrame({
            "Metric": ["Levene’s Statistic", "p-value", "Max/Min Variance Ratio"],
            "Value": [f"{stat:.4f}", f"{p:.6f}", f"{ratio:.2f}"]
        })
        display(summary_df.style
                .background_gradient(subset=["Value"], cmap="Blues")
                .set_caption(
            f'<b><span style="font-size:14px; text-align:center; display:block;">'
            f'Homogeneity of Variance — {feature} by {target_feature}</span></b>'
        ).set_table_attributes('style="width:70%; margin:auto;"'))

        # Print interpretation
        logger.info("Interpretation:")
        logger.info(f"- Status: {status}")
        logger.info(f"- Recommendation: {recommendation}")

        return anova_use, is_homogeneous_variances

    @staticmethod
    def cal_mannwhitneyu(dataframe: pd.DataFrame, categorical_feature: str, 
                        num_feature: str, logger: logging.Logger) -> None:
        """
        Perform the Mann–Whitney U test (Wilcoxon rank-sum test) to assess whether there 
        is a statistically significant difference in the distribution of a numerical feature 
        between two independent groups defined by a binary categorical feature.

        The function also compares medians, calculates the effect size (r), provides interpretation,

        Parameters
        ----------
        dataframe : pd.DataFrame
            The input DataFrame containing the data.

        categorical_feature : str
            Column name of the categorical feature (must contain exactly 2 unique values).

        num_feature : str
            Column name of the numerical feature to compare.

        logger : logging.Logger
            Logger instance used to record the analysis process, statistical results,
            and decision messages.

        Returns
        -------
        None
            Prints the U statistic, p-value, medians, Z-score, effect size r, and interpretation.

        Notes
        -----
        - H₀ (Null Hypothesis): The two groups have the same distribution.
        - H₁ (Alternative Hypothesis): The distributions are different.
        - If p ≤ 0.05 → reject H₀ → significant difference.
        - Effect size r helps interpret how strong the difference is:
            * Small ~0.1, Medium ~0.3, Large ≥0.5
        """
        groups = dataframe[categorical_feature].dropna().unique()

        # Validation check
        if len(groups) != 2:
            logger.error(f"Mann–Whitney U test requires exactly 2 groups, but found {len(groups)}.")
            return

        logger.info(f"Running Mann–Whitney U Test: '{num_feature}' by '{categorical_feature}'...")
        logger.debug(f"Number of groups detected: {len(groups)}")

        group1 = dataframe[dataframe[categorical_feature] == groups[0]][num_feature].dropna()
        group2 = dataframe[dataframe[categorical_feature] == groups[1]][num_feature].dropna()

        n1, n2 = len(group1), len(group2)

        stat, p = mannwhitneyu(group1, group2, alternative="two-sided")

        logger.info(f"U statistic: {stat}")
        logger.info(f"p-value    : {p:.6f}")

        # Effect size (r)
        mean_U = n1 * n2 / 2
        std_U = np.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
        z = (stat - mean_U) / std_U
        r = abs(z) / np.sqrt(n1 + n2)

        # Interpretation
        if p <= 0.05:
            logger.info("Result: p-value ≤ 0.05 → Reject H0")
            logger.info("Conclusion: Significant difference between the two groups.")

            if r < 0.1:
                logger.info("Effect size interpretation: Negligible")
            elif r < 0.3:
                logger.info("Effect size interpretation: Small")
            elif r < 0.5:
                logger.info("Effect size interpretation: Medium")
            else:
                logger.info("Effect size interpretation: Large")
        else:
            logger.warning("Result: p-value > 0.05 → Fail to reject H0")
            logger.warning("Conclusion: No statistically significant difference detected.")

    @staticmethod
    def t_test_with_cohens_d(data: pd.DataFrame, logger: logging.Logger, categorical_feature: str, 
                             num_feature: str, equal_var: bool=False) -> None:
        """
        Perform an Independent Two-Sample T-Test and compute Cohen's d to evaluate 
        the difference between two independent groups on a numeric variable.

        Supports both:
        - Student’s T-Test (equal variances)
        - Welch’s T-Test (unequal variances, default)

        Parameters
        ----------
        data : pd.DataFrame
            The input DataFrame containing the categorical and numerical features.

        logger : logging.Logger
            Logger instance used to record the analysis process, statistical results,
            and decision messages.

        categorical_feature : str
            The name of the categorical column used to define the two groups (must have exactly 2 unique values).

        num_feature : str
            The name of the numerical feature to compare between the two groups.

        equal_var : bool, optional (default=False)
            If True → Student’s t-test (equal variances).
            If False → Welch’s t-test (unequal variances).

        Returns
        -------
        None
            Prints the t-statistic, p-value, Cohen’s d, and interpretation of the effect size.

        Notes
        -----
        - H₀ (null hypothesis): The two groups have equal means.
        - H₁ (alternative): The group means differ significantly.
        - Cohen's d interpretation:
            - 0.2 → small effect
            - 0.5 → medium effect
            - 0.8+ → large effect
        - Welch’s t-test is recommended when group variances are unequal (default setting).

        References
        ----------
        - https://www.scribbr.com/statistics/t-test/
        - https://en.wikipedia.org/wiki/Welch%27s_t-test
        - https://en.wikipedia.org/wiki/Cohen%27s_d
        """

        # Extract unique groups
        groups = data[categorical_feature].dropna().unique()

        if len(groups) != 2:
            logger.error("Independent T-Test requires exactly 2 groups.")
            return

        test_type = (
            "Student’s T-Test (equal variances)" 
            if equal_var 
            else "Welch’s T-Test (unequal variances)"
        )

        logger.info(f"Running Independent Two-Sample T-Test: '{num_feature}' ~ '{categorical_feature}'")
        logger.debug(f"Number of groups detected: {len(groups)}")
        logger.debug(f"Test Type: {test_type}")

        # Extract values
        x1 = data[data[categorical_feature] == groups[0]][num_feature].dropna()
        x2 = data[data[categorical_feature] == groups[1]][num_feature].dropna()

        # Run T-Test
        t_stat, p_value = ttest_ind(x1, x2, equal_var=equal_var)

        # Calculate Cohen's d (different formulas depending on variance assumption)
        nx1, nx2 = len(x1), len(x2)
        s1, s2 = np.var(x1, ddof=1), np.var(x2, ddof=1)

        if equal_var:
            # --- Student’s T-Test version (pooled variance)
            pooled_std = np.sqrt(((nx1 - 1) * s1 + (nx2 - 1) * s2) / (nx1 + nx2 - 2))
            cohens_d = (np.mean(x1) - np.mean(x2)) / pooled_std
        else:
            # --- Welch’s T-Test version (average variance)
            s_pooled = np.sqrt((s1 + s2) / 2)
            cohens_d = (np.mean(x1) - np.mean(x2)) / s_pooled

        # Display results
        logger.info(f"Comparing groups: '{groups[0]}' vs '{groups[1]}'")
        logger.info(f"p-value: {p_value:.6f}")
        logger.info(f"Cohen's d: {cohens_d:.3f}")
        logger.debug(f"t-statistic: {t_stat:.3f}")
        logger.debug(f"Group means → {groups[0]}: {x1.mean():.3f}, {groups[1]}: {x2.mean():.3f}")

        # Significance interpretation
        if p_value < 0.05:
            logger.info("Result: p-value ≤ 0.05 → Reject H0")
            logger.info("Conclusion: Significant difference between the two groups.")
            # Effect size interpretation
            abs_d = abs(cohens_d)
            if abs_d < 0.2:
                effect_label = "small"
            elif abs_d < 0.5:
                effect_label = "medium"
            else:
                effect_label = "large"

            logger.info(f"Effect size interpretation: {effect_label} effect (|d| = {abs_d:.3f})")
        else:
            logger.warning("Result: p-value > 0.05 → Fail to reject H0")
            logger.warning("Conclusion: No statistically significant difference detected.")

    @staticmethod
    def perform_statical_testing(feature: str, df: pd.DataFrame, target_feature: str, 
                                 logger: logging.Logger) -> None:
        """
        Run statistical tests to determine whether a numerical feature differs
        across categories of a target variable.

        The function automatically selects appropriate tests based on:
        - Normality of the feature distribution
        - Homogeneity of variances
        - Number of categories in the target variable

        Possible tests include:
        - ANOVA or Welch’s ANOVA
        - Kruskal–Wallis test
        - Independent T-test (Student or Welch)
        - Mann–Whitney U test

        Parameters
        ----------
        feature : str
            Numerical feature to be tested.

        df : pd.DataFrame
            Input dataset containing the feature and target variable.

        target_feature : str
            Categorical variable used to group the data.

        logger : logging.Logger
            Logger instance used to record the analysis process, statistical results,
            and decision messages.

        Returns
        -------
        None
            Executes statistical tests and prints the results.
        """

        # Step 1 — Check whether the numerical feature follows a normal distribution
        # The function also generates diagnostic plots for visualization
        non_normal_detected = StatUtils.check_normality_with_plots(df=df, logger=logger, feature=feature, target_feature=target_feature)

        # Step 2 — Determine number of unique categories in the target variable
        # This decides whether we perform a 2-group test or multi-group test
        total_categories = df[target_feature].nunique()

        # CASE 1 — Target variable has more than 2 groups
        if total_categories > 2:
            if non_normal_detected:
                # If the distribution is non-normal → use a non-parametric test
                StatUtils.perform_kruskal_test(df=df, categorical_feature=target_feature,
                                               numeric_feature=feature, logger=logger)
            else:
                # Step 3 — Check homogeneity of variance (Levene test typically)
                anove_use, is_homogeneous_variances = StatUtils.check_homogeneity_of_variance(df=df, logger=logger,
                                                                                              feature=feature, target_feature=target_feature)
                # If normal distribution + equal variances → standard ANOVA
                if anove_use and is_homogeneous_variances:
                    StatUtils.perform_anova_with_tukey(df=df, logger=logger, numeric_feature=feature,
                                            categorical_feature=target_feature)
                # If normal distribution but unequal variances → Welch ANOVA
                elif anove_use and is_homogeneous_variances == False:
                    StatUtils.perform_welch_anova(df=df, logger=logger, numeric_feature=feature, categorical_feature=target_feature)
                # Fallback to non-parametric test
                else:
                    StatUtils.perform_kruskal_test(df=df, categorical_feature=target_feature,
                                                   numeric_feature=feature, logger=logger)
        # CASE 2 — Target variable has exactly 2 groups
        else:
            # Non-normal distribution → Mann–Whitney U test
            if non_normal_detected == True:
                StatUtils.cal_mannwhitneyu(dataframe=df, categorical_feature=target_feature, num_feature=feature, logger=logger)
            else:
                # Check variance equality to determine type of t-test
                anove_use, is_homogeneous_variances = StatUtils.check_homogeneity_of_variance(df=df, logger=logger, feature=feature,
                                                                                    target_feature=target_feature)
                # Equal variances → Student's T-Test
                if anove_use and is_homogeneous_variances:
                    StatUtils.t_test_with_cohens_d(data=df, logger=logger, categorical_feature=target_feature, num_feature=feature, equal_var=True)
                # Unequal variances → Welch's T-Test
                elif anove_use and is_homogeneous_variances == False:
                    StatUtils.t_test_with_cohens_d(data=df, logger=logger, categorical_feature=target_feature, num_feature=feature, equal_var=False)
                # Fallback to Mann–Whitney U test
                else:
                    StatUtils.cal_mannwhitneyu(dataframe=df, categorical_feature=target_feature, num_feature=feature, logger=logger)

    @staticmethod
    def analyze_numeric_feature_by_target(feature: str, df: pd.DataFrame, logger: logging.Logger,
                                          target_feature: str, order: list = None) -> None:
        """
        Analyze and visualize the distribution of a numerical feature across
        categories of a target variable.

        The function performs:
        1. Descriptive statistics summary.
        2. Statistical significance testing between groups.
        3. Distribution visualization using a violin plot.

        Parameters
        ----------
        feature : str
            Numerical feature to analyze.

        df : pd.DataFrame
            Input dataset containing the numerical feature and target variable.

        logger : logging.Logger
            Logger instance used to record the analysis process, statistical results,
            and decision messages.

        target_feature : str
            Categorical feature used to group the data.

        order : list, optional
            Custom ordering of target categories for visualization.

        Returns
        -------
        None
            Displays summary statistics, statistical test results,
            and distribution plots.
        """

        # Step 1 — Compute descriptive statistics per target group
        df_summary_feature = (
            df.groupby(by=target_feature, as_index=False)
            .agg(
                Count=(feature, "count"),
                Mean=(feature, "mean"),
                Median=(feature, "median"),
                Std=(feature, "std")
            )
            .sort_values(by="Mean", ascending=False).reset_index(drop=True)
        )

        # Step 2 — Compute overall statistics for the feature
        summary_data = [
            ("Overall Mean", f"{df[feature].mean():.2f}"),
            ("Overall Median", f"{df[feature].median()}"),
            ("Overall Std", f"{df[feature].std():.2f}")
        ]

        # Display overall statistics as formatted HTML list
        summary_html = "<ul>" + "".join([
            f"<li><b>{k}:</b> {v}</li>" for k, v in summary_data
        ]) + "</ul>"
        display(HTML(summary_html))

        # Step 3 — Display summary table with color gradient
        display(
            df_summary_feature.style.background_gradient(cmap=sns.light_palette("blue", as_cmap=True))
            .set_table_attributes('style="width:75%; margin:auto;"')
        )

        # Step 4 — Perform statistical significance testing
        StatUtils.perform_statical_testing(feature=feature, df=df, logger=logger, target_feature=target_feature)

        # Step 5 — Visualize distribution using violin plot
        plt.figure(figsize=(10, 6))
        sns.violinplot(x=target_feature, y=feature, data=df, hue=target_feature, order=order,
                       palette=ColorUtils.color(n_colors=df[target_feature].nunique(), tone="diverging"))
        
        plt.title(f"Violin plot of {feature} distribution by Subscription ({target_feature})",
                  pad=15, weight="bold", fontsize=12)
        plt.xlabel("")
        plt.ylabel("")
        plt.legend().remove()
        sns.despine(left=False, bottom=False)
        plt.tight_layout()
        plt.show()

    def analyze_categorical_feature_vs_target(cat: str, target_feature: str, logger: logging.Logger, 
                                              df: pd.DataFrame, figsize=(20, 6), order=None) -> None:
        """
        Plot the relationship between a categorical feature and the target variable.

        This function displays:
        - A stacked bar chart showing percentage distribution of target classes.
        - A count plot showing absolute frequencies.
        - A Chi-Square test for feature–target dependence.

        Parameters
        ----------
        cat : str
            Categorical feature name.

        target_feature : str
            Target variable name.

        logger : logging.Logger
            Logger instance used to record the analysis process, statistical results,
            and decision messages.

        df : pd.DataFrame
            Input dataset.

        figsize : tuple, optional
            Figure size (width, height). Default is (15, 6).

        order : list, optional
            Custom order of categories on x-axis.

        Returns
        -------
        None
        """

        display(HTML(f"<h2 style='text-align:center; font-size:22px; color:blue;'><b>Distribution of {cat.title()} by {target_feature.title()}</b></h2>"))
        fig, ax = plt.subplots(nrows=1, ncols=2, sharey=False, figsize=figsize)

        # Data processing
        grouped = df.groupby([cat, target_feature]).size().unstack(fill_value=0)

        # Define a fixed hue order (adjust if needed)
        target_order = [c for c in ["Yes", "No"] if c in grouped.columns]

        # Fallback if the labels are 0/1 or have different names
        if not target_order:
            target_order = list(grouped.columns)

        # Calculate percentages row-wise and reorder columns by target_order
        percentages = grouped.div(grouped.sum(axis=1), axis=0)[target_order] * 100

        # Define X-axis category order
        if order is not None:
            percentages = percentages.loc[order]
            labels = order
        else:
            labels = percentages.index.tolist()

        # Consistent color palette for both charts
        base_colors = ColorUtils.color(n_colors=len(target_order))
        color_map = dict(zip(target_order, base_colors))

        # Plot 1: Stacked bar chart (percentage)
        bottom = np.zeros(len(percentages))
        for cls in target_order:
            ax[0].bar(percentages.index.astype(str), percentages[cls].values, bottom=bottom,
                    label=cls, color=color_map[cls])
            bottom += percentages[cls].values

        # Add percentage labels
        for container in ax[0].containers:
            ax[0].bar_label(container, fmt="%1.0f%%", label_type="center",
                            fontsize=10, color="black")

        ax[0].set_title(f"Subscription Rate Across {cat.replace('_', ' ').title()}", fontsize=12, weight="bold", pad=15)
        ax[0].set_xlabel(f"{cat}", fontsize=10)
        ax[0].set_ylabel(f"% {target_feature} Rate", fontsize=10)
        ax[0].set_xticklabels(labels = labels, rotation = 45)
        sns.despine(left=False, bottom=False, ax=ax[0])
        ax[0].legend().remove()

        # Plot 2: Count plot (using same color_map + hue_order)
        sns.countplot(data=df, hue=target_feature, x=cat,
                    order=labels, hue_order=target_order,
                    palette=color_map, ax=ax[1])

        for container in ax[1].containers:
            ax[1].bar_label(container, fmt="%d", label_type="edge",
                            fontsize=10, color="black")

        ax[1].set_title(f"Subscription Count by {cat.replace('_', ' ').title()}", fontsize=12, weight="bold", pad=15)
        ax[1].set_xlabel(f"{cat}", fontsize=10)
        ax[1].set_ylabel("Number of Customers", fontsize=10)
        ax[1].legend(title=target_feature, bbox_to_anchor=(1.05, 1), loc="upper left")
        ax[1].set_xticklabels(labels = ax[1].get_xticklabels(), rotation = 45)
        sns.despine(left=False, bottom=False, ax=ax[1])
        plt.tight_layout()
        plt.show()

        # Chi-Square Test
        StatUtils.cal_ChiSquare(cat_feature=cat, target_feature=target_feature, df=df, logger=logger, show_residuals=True)
