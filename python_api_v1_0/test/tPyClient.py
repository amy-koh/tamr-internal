#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 20:28:49 2018

@author: akoh
"""

import unittest
import unify_api_v1 as unifyapi

from unify_api_v1.auth import UsernamePasswordAuth

class TestPyClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create client object. """
        username = 'admin'
        password = 'dt'
        ipaddr = '10.20.0.189'  
        auth = UsernamePasswordAuth(username, password)
        cls.unify = unifyapi.Client(auth, host=ipaddr)

    def test_dataset(self):
        """Test API for retrieving datasets."""
        dataset_name = 'USA-spending.csv'
        dataset = self.unify.datasets.by_name(dataset_name)
        
        expected = dataset_name
        actual = dataset.name
        self.assertEqual(expected, actual)
        
        dataset_id = dataset.api_path
        dataset = self.unify.datasets.by_relative_id(dataset_id)
        
        self.assertEqual(expected, actual)
                
    def test_project(self):
        """Test API for retrieving projects and metadata."""
        dataset_name = 'USA-spending.csv'
        project_id = 'projects/1'
        project = self.unify.projects.by_relative_id(project_id)
        
        expected = 'MasteringTutorial'
        actual = project.name
        self.assertEqual(expected, actual)
        
        expected = 'Mastering Project'
        actual = project.description
        self.assertEqual(expected, actual)
    
    def test_project_dataset(self):
        """Test API for retrieving input and unified datasets."""
        project_id = 'projects/2'
        project = self.unify.projects.by_relative_id(project_id)
        
        expected = 'SMTutorial'
        actual = project.name
        self.assertEqual(expected, actual)
        
        expected = 'Schema Mapping Recommendations Project'
        actual = project.description
        self.assertEqual(expected, actual)
  
  	#TODO: Comment out due to bug in API
        #input_datasets = project.input_datasets()     
        unified_dataset = project.unified_dataset()
        
        expected = 'SMTutorial_unified_dataset'
        actual = unified_dataset.name
        self.assertEqual(expected, actual)
    
        op = unified_dataset.refresh()
        self.assertTrue(op.succeeded())
        self.assertEqual(op.state, 'SUCCEEDED')
        
    def test_categorisations(self):
        """Test API for categorisation workflow."""
        project_id = 'projects/3'
        project = self.unify.projects.by_relative_id(project_id)
        
        expected = 'CatTutorial'
        actual = project.name
        self.assertEqual(expected, actual)
        
        expected = 'Categorization Project'
        actual = project.description
        self.assertEqual(expected, actual)
        
        catModel = project.categorizations().model()
        op = catModel.refresh()
        self.assertTrue(op.succeeded())
        
        catDatasets = project.categorizations()
        op = catDatasets.refresh()
        self.assertTrue(op.succeeded())
         
    @classmethod
    def tearDownClass(cls):
        """Delete client object."""
        del(cls.unify)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
