import numpy as np
from sklearn.model_selection import RandomizedSearchCV
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
import json
import os
from datetime import datetime

class BaseModels:
    def __init__(self, random_state=42):
        self.random_state = random_state
        
        # Define parameter grids
        self.xgb_params = {
            'max_depth': [3, 5, 7, 9],
            'learning_rate': [0.01, 0.05, 0.1],
            'n_estimators': [100, 200, 300],
            'subsample': [0.8, 0.9, 1.0],
            'colsample_bytree': [0.8, 0.9, 1.0]
        }

        self.rf_params = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 20, 30, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }

        self.lgbm_params = {
            'num_leaves': [31, 50, 70],
            'learning_rate': [0.01, 0.05, 0.1],
            'n_estimators': [100, 200, 300],
            'max_depth': [-1, 5, 10]
        }

        # Initialize best models dict
        self.best_models = {}
        self.best_params = {}
        self.cv_results = {}

    def train_xgboost(self, X_train, y_train, n_iter=20):
        """Train XGBoost model with RandomizedSearchCV"""
        xgb_model = xgb.XGBClassifier(random_state=self.random_state)
        
        search = RandomizedSearchCV(
            xgb_model,
            self.xgb_params,
            n_iter=n_iter,
            cv=5,
            random_state=self.random_state,
            scoring='f1_weighted',
            n_jobs=-1
        )
        
        search.fit(X_train, y_train)
        
        self.best_models['xgboost'] = search.best_estimator_
        self.best_params['xgboost'] = search.best_params_
        self.cv_results['xgboost'] = {
            'best_score': search.best_score_,
            'best_params': search.best_params_
        }
        
        return search.best_estimator_

    def train_random_forest(self, X_train, y_train, n_iter=20):
        """Train Random Forest model with RandomizedSearchCV"""
        rf_model = RandomForestClassifier(random_state=self.random_state)
        
        search = RandomizedSearchCV(
            rf_model,
            self.rf_params,
            n_iter=n_iter,
            cv=5,
            random_state=self.random_state,
            scoring='f1_weighted',
            n_jobs=-1
        )
        
        search.fit(X_train, y_train)
        
        self.best_models['random_forest'] = search.best_estimator_
        self.best_params['random_forest'] = search.best_params_
        self.cv_results['random_forest'] = {
            'best_score': search.best_score_,
            'best_params': search.best_params_
        }
        
        return search.best_estimator_

    def train_lightgbm(self, X_train, y_train, n_iter=20):
        """Train LightGBM model with RandomizedSearchCV"""
        lgb_model = lgb.LGBMClassifier(random_state=self.random_state)
        
        search = RandomizedSearchCV(
            lgb_model,
            self.lgbm_params,
            n_iter=n_iter,
            cv=5,
            random_state=self.random_state,
            scoring='f1_weighted',
            n_jobs=-1
        )
        
        search.fit(X_train, y_train)
        
        self.best_models['lightgbm'] = search.best_estimator_
        self.best_params['lightgbm'] = search.best_params_
        self.cv_results['lightgbm'] = {
            'best_score': search.best_score_,
            'best_params': search.best_params_
        }
        
        return search.best_estimator_

    def train_all_models(self, X_train, y_train, n_iter=20):
        """Train all three models"""
        print("Training XGBoost...")
        self.train_xgboost(X_train, y_train, n_iter)
        
        print("Training Random Forest...")
        self.train_random_forest(X_train, y_train, n_iter)
        
        print("Training LightGBM...")
        self.train_lightgbm(X_train, y_train, n_iter)

    def save_results(self, dataset_name):
        """Save training results and best parameters"""
        results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'dataset': dataset_name,
            'cv_results': self.cv_results,
            'best_parameters': self.best_params
        }
        
        # Create results directory if it doesn't exist
        os.makedirs('results', exist_ok=True)
        
        # Save results
        filename = f'results/base_models_{dataset_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"Results saved to {filename}")

    def get_feature_importance(self, feature_names):
        """Get feature importance for all models"""
        importance_dict = {}
        
        # XGBoost feature importance
        if 'xgboost' in self.best_models:
            xgb_importance = self.best_models['xgboost'].feature_importances_
            importance_dict['xgboost'] = dict(zip(feature_names, xgb_importance))
        
        # Random Forest feature importance
        if 'random_forest' in self.best_models:
            rf_importance = self.best_models['random_forest'].feature_importances_
            importance_dict['random_forest'] = dict(zip(feature_names, rf_importance))
        
        # LightGBM feature importance
        if 'lightgbm' in self.best_models:
            lgb_importance = self.best_models['lightgbm'].feature_importances_
            importance_dict['lightgbm'] = dict(zip(feature_names, lgb_importance))
        
        return importance_dict