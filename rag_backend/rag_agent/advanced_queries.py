"""
Advanced query capabilities for employee data
"""
import pandas as pd
from typing import List, Dict, Any, Optional
import re
from datetime import datetime

class EmployeeQueryEngine:
    """Advanced query engine for employee data"""
    
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load employee data from Excel"""
        try:
            self.df = pd.read_excel(self.excel_path)
            # Clean column names
            self.df.columns = [col.strip().lower().replace(' ', '_') for col in self.df.columns]
        except Exception as e:
            print(f"Error loading Excel data: {e}")
            self.df = pd.DataFrame()
    
    def search_by_name(self, name: str) -> List[Dict]:
        """Search employees by name (partial match)"""
        if self.df.empty:
            return []
        
        # Case-insensitive partial match
        mask = self.df['name'].str.contains(name, case=False, na=False)
        results = self.df[mask].to_dict('records')
        return results
    
    def search_by_department(self, department: str) -> List[Dict]:
        """Search employees by department"""
        if self.df.empty:
            return []
        
        mask = self.df['department'].str.contains(department, case=False, na=False)
        results = self.df[mask].to_dict('records')
        return results
    
    def search_by_role(self, role: str) -> List[Dict]:
        """Search employees by role/title"""
        if self.df.empty:
            return []
        
        mask = self.df['title'].str.contains(role, case=False, na=False)
        results = self.df[mask].to_dict('records')
        return results
    
    def get_department_stats(self) -> Dict[str, Any]:
        """Get statistics by department"""
        if self.df.empty:
            return {}
        
        dept_stats = self.df.groupby('department').agg({
            'name': 'count',
            'title': lambda x: list(x.unique())
        }).rename(columns={'name': 'employee_count', 'title': 'roles'})
        
        return dept_stats.to_dict('index')
    
    def get_seniority_analysis(self) -> Dict[str, Any]:
        """Analyze employee seniority based on start dates"""
        if self.df.empty or 'start_date' not in self.df.columns:
            return {}
        
        try:
            # Convert start dates to datetime
            self.df['start_date'] = pd.to_datetime(self.df['start_date'], errors='coerce')
            
            # Calculate years of service
            current_date = datetime.now()
            self.df['years_of_service'] = (current_date - self.df['start_date']).dt.days / 365.25
            
            # Categorize by seniority
            def categorize_seniority(years):
                if years < 1:
                    return 'New Hire (< 1 year)'
                elif years < 3:
                    return 'Junior (1-3 years)'
                elif years < 7:
                    return 'Mid-level (3-7 years)'
                else:
                    return 'Senior (7+ years)'
            
            self.df['seniority_level'] = self.df['years_of_service'].apply(categorize_seniority)
            
            seniority_stats = self.df.groupby('seniority_level').agg({
                'name': 'count',
                'years_of_service': ['mean', 'min', 'max']
            }).round(2)
            
            return seniority_stats.to_dict()
            
        except Exception as e:
            print(f"Error in seniority analysis: {e}")
            return {}
    
    def search_by_experience(self, min_years: float = None, max_years: float = None) -> List[Dict]:
        """Search employees by experience level"""
        if self.df.empty or 'start_date' not in self.df.columns:
            return []
        
        try:
            # Calculate years of service if not already done
            if 'years_of_service' not in self.df.columns:
                self.df['start_date'] = pd.to_datetime(self.df['start_date'], errors='coerce')
                current_date = datetime.now()
                self.df['years_of_service'] = (current_date - self.df['start_date']).dt.days / 365.25
            
            # Filter by experience
            mask = True
            if min_years is not None:
                mask &= self.df['years_of_service'] >= min_years
            if max_years is not None:
                mask &= self.df['years_of_service'] <= max_years
            
            results = self.df[mask].to_dict('records')
            return results
            
        except Exception as e:
            print(f"Error in experience search: {e}")
            return []
    
    def get_company_overview(self) -> Dict[str, Any]:
        """Get comprehensive company overview"""
        if self.df.empty:
            return {}
        
        overview = {
            'total_employees': len(self.df),
            'departments': self.df['department'].nunique() if 'department' in self.df.columns else 0,
            'unique_titles': self.df['title'].nunique() if 'title' in self.df.columns else 0,
        }
        
        # Add department breakdown
        if 'department' in self.df.columns:
            dept_breakdown = self.df['department'].value_counts().to_dict()
            overview['department_breakdown'] = dept_breakdown
        
        # Add seniority analysis
        seniority = self.get_seniority_analysis()
        if seniority:
            overview['seniority_breakdown'] = seniority
        
        return overview
    
    def parse_natural_language_query(self, query: str) -> Dict[str, Any]:
        """Parse natural language queries into structured search parameters"""
        query_lower = query.lower()
        
        # Extract patterns
        patterns = {
            'department': r'(?:in|from|of|at)\s+(\w+(?:\s+\w+)*?)\s+(?:department|dept)',
            'role': r'(?:as|with|title|role)\s+(?:of\s+)?(\w+(?:\s+\w+)*?)(?:\s+in|\s+at|$)',
            'experience': r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)',
            'seniority': r'(senior|junior|mid-level|new|experienced)',
            'name': r'(?:find|search|who\s+is)\s+(\w+(?:\s+\w+)*)'
        }
        
        extracted = {}
        
        for key, pattern in patterns.items():
            match = re.search(pattern, query_lower)
            if match:
                extracted[key] = match.group(1).strip()
        
        return extracted

# Example usage functions
def get_employee_by_email(email: str, df: pd.DataFrame) -> Optional[Dict]:
    """Get employee by email address"""
    if df.empty or 'email' not in df.columns:
        return None
    
    mask = df['email'].str.lower() == email.lower()
    result = df[mask]
    
    if len(result) > 0:
        return result.iloc[0].to_dict()
    return None

def get_employees_by_location(location: str, df: pd.DataFrame) -> List[Dict]:
    """Get employees by location (if location data exists)"""
    if df.empty or 'location' not in df.columns:
        return []
    
    mask = df['location'].str.contains(location, case=False, na=False)
    results = df[mask].to_dict('records')
    return results 