from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Healthcare Pipeline Dashboard</title>
            <!-- Load React first -->
            <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
            <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
            
            <!-- Load Dependencies for Recharts -->
            <script src="https://unpkg.com/prop-types@15.8.1/prop-types.min.js"></script>
            
            <!-- Load Recharts -->
            <script src="https://unpkg.com/recharts@2.1.12/umd/Recharts.js"></script>
            
            <!-- Load Tailwind -->
            <script src="https://cdn.tailwindcss.com"></script>
            <script>
                tailwind.config = {
                    darkMode: 'class',
                    theme: {
                        extend: {}
                    }
                }
            </script>
            
            <!-- Load Babel -->
            <script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
            
            <style>
                #root { min-height: 100vh; width: 100%; }
            </style>
        </head>
        <body>
            <div id="root"></div>
            <script type="text/babel" src="/static/dashboard.js"></script>
        </body>
    </html>
    """