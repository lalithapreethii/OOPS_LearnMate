    def create_weakness_levels(self, df: pd.DataFrame, score_column: str) -> pd.DataFrame:
        """Create weakness levels based on performance scores"""
        self.logger.info("Creating weakness level target...")
        
        # Calculate percentile ranks
        ranks = df[score_column].rank(pct=True)
        
        # Create weakness levels (0: Weak, 1: Moderate, 2: Strong)
        conditions = [
            (ranks >= self.weakness_thresholds['strong']),  # Strong
            (ranks >= self.weakness_thresholds['moderate']) & (ranks < self.weakness_thresholds['strong']),  # Moderate
            (ranks < self.weakness_thresholds['moderate'])  # Weak
        ]
        choices = [2, 1, 0]
        
        df['weakness_level'] = np.select(conditions, choices, default=1)
        
        # Log distribution
        dist = df['weakness_level'].value_counts()
        self.logger.info(f"Weakness level distribution:\n{dist}")
        self.report['class_distribution'] = dist.to_dict()
        
        return df