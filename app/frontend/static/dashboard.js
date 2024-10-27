// Log dependencies for debugging
console.log('Dependencies check:', {
  Recharts: typeof Recharts !== 'undefined',
  React: typeof React !== 'undefined',
  ReactDOM: typeof ReactDOM !== 'undefined'
});

// Destructure Recharts components
const {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} = Recharts;

// Add dark mode toggle function
const toggleDarkMode = () => {
  document.documentElement.classList.toggle('dark');
};

// Generate mock data
const generateMockData = () => {
  return Array.from({ length: 24 }, (_, i) => ({
    time: `${String(i).padStart(2, '0')}:00`,
    responseTime: Math.floor(Math.random() * 50 + 150),
    errorRate: Math.random() * 2,
    authAttempts: Math.floor(Math.random() * 100),
    successfulAuth: Math.floor(Math.random() * 90)
  }));
};

// Dashboard Metric Component
const DashboardMetric = ({ icon, title, value, description }) => (
  <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow transition-colors">
    <div className="flex items-center justify-between">
      <div className="space-y-1">
        <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
        <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
        <p className="text-xs text-gray-400 dark:text-gray-500">{description}</p>
      </div>
      <span className="text-2xl">{icon}</span>
    </div>
  </div>
);

// Main Dashboard Component
const Dashboard = () => {
  const mockData = generateMockData();

  return (
    <div className="p-6 space-y-6 bg-gray-50 dark:bg-gray-900 min-h-screen transition-colors">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Healthcare Pipeline Monitoring</h1>
        <button
          onClick={toggleDarkMode}
          className="px-4 py-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 transition-colors"
        >
          Toggle Theme
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <DashboardMetric
          icon="⚡"
          title="System Health"
          value="99.98%"
          description="All systems operational"
        />
        <DashboardMetric
          icon="🛡️"
          title="Security Score"
          value="A+"
          description="HIPAA Compliant"
        />
        <DashboardMetric
          icon="⚠️"
          title="Active Alerts"
          value="0"
          description="No critical issues"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow transition-colors">
          <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">API Response Times</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockData}>
                <CartesianGrid strokeDasharray="3 3" className="dark:opacity-40" />
                <XAxis
                  dataKey="time"
                  stroke="#888"
                  className="dark:text-gray-300"
                />
                <YAxis
                  stroke="#888"
                  className="dark:text-gray-300"
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    border: 'none',
                    borderRadius: '4px',
                    boxShadow: '0 2px 5px rgba(0,0,0,0.2)'
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="responseTime"
                  stroke="#2196F3"
                  name="Response Time (ms)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow transition-colors">
          <h2 className="text-lg font-semibold mb-4 text-gray-800 dark:text-white">Authentication Metrics</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockData}>
                <CartesianGrid strokeDasharray="3 3" className="dark:opacity-40" />
                <XAxis
                  dataKey="time"
                  stroke="#888"
                  className="dark:text-gray-300"
                />
                <YAxis
                  stroke="#888"
                  className="dark:text-gray-300"
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    border: 'none',
                    borderRadius: '4px',
                    boxShadow: '0 2px 5px rgba(0,0,0,0.2)'
                  }}
                />
                <Legend />
                <Bar dataKey="authAttempts" fill="#4CAF50" name="Total Attempts" />
                <Bar dataKey="successfulAuth" fill="#2196F3" name="Successful Auth" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

// Render with error handling
try {
  console.log('Finding root element...');
  const rootElement = document.getElementById('root');
  console.log('Root element found:', rootElement);

  console.log('Creating React root...');
  const root = ReactDOM.createRoot(rootElement);

  console.log('Rendering Dashboard...');
  root.render(
    <React.StrictMode>
      <Dashboard />
    </React.StrictMode>
  );

  console.log('Render completed successfully');
} catch (error) {
  console.error('Error during render:', error);
  console.error('Error details:', {
    message: error.message,
    stack: error.stack
  });
}