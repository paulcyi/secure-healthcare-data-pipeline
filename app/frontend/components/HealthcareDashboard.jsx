// File: app/frontend/components/HealthcareDashboard.jsx
import React from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Shield, Activity, Users, AlertTriangle } from 'lucide-react';

// Generate 24 hours of mock data
const mockTimeData = Array.from({ length: 24 }, (_, i) => ({
  time: `${String(i).padStart(2, '0')}:00`,
  responseTime: Math.floor(Math.random() * 50 + 150),
  errorRate: Math.random() * 2,
  authAttempts: Math.floor(Math.random() * 100),
  successfulAuth: Math.floor(Math.random() * 90)
}));

const DashboardMetric = ({ icon: Icon, title, value, description, color = "text-blue-500" }) => (
  <Card className="bg-white">
    <CardContent className="p-6">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <p className="text-sm text-gray-500">{title}</p>
          <p className="text-2xl font-bold">{value}</p>
          <p className="text-xs text-gray-400">{description}</p>
        </div>
        <Icon className={`h-8 w-8 ${color}`} />
      </div>
    </CardContent>
  </Card>
);

export default function HealthcareDashboard() {
  return (
    <div className="p-6 space-y-6 bg-gray-50 min-h-screen">
      <h1 className="text-2xl font-bold text-gray-800">Healthcare Pipeline Monitoring</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <DashboardMetric
          icon={Activity}
          title="System Health"
          value="99.98%"
          description="All systems operational"
          color="text-green-500"
        />
        <DashboardMetric
          icon={Shield}
          title="Security Score"
          value="A+"
          description="HIPAA Compliant"
          color="text-blue-500"
        />
        <DashboardMetric
          icon={AlertTriangle}
          title="Active Alerts"
          value="0"
          description="No critical issues"
          color="text-orange-500"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold">API Response Times (ms)</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={mockTimeData}>
                  <CartesianGrid strokeDasharray="3 3" className="opacity-50" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="responseTime"
                    stroke="#2196F3"
                    strokeWidth={2}
                    name="Response Time (ms)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Authentication Metrics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={mockTimeData}>
                  <CartesianGrid strokeDasharray="3 3" className="opacity-50" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="authAttempts" fill="#4CAF50" name="Total Attempts" />
                  <Bar dataKey="successfulAuth" fill="#2196F3" name="Successful Auth" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}