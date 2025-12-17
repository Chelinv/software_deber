import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from main import app
    from app.api.endpoints import financial_controller, report_controller
    from app.services.financial_service import FinancialService
    from app.services.report_service import ReportService
    print("Successfully imported app and new modules.")
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc()
