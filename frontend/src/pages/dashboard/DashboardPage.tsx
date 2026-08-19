import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', revenue: 4000, bookings: 24 },
  { month: 'Feb', revenue: 3000, bookings: 21 },
  { month: 'Mar', revenue: 2000, bookings: 29 },
  { month: 'Apr', revenue: 2780, bookings: 32 },
  { month: 'May', revenue: 1890, bookings: 28 },
  { month: 'Jun', revenue: 2390, bookings: 35 },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-card p-6 rounded-lg border border-border shadow-sm">
          <p className="text-sm text-muted-foreground mb-1">Total Revenue</p>
          <p className="text-2xl font-bold text-primary">$15,234</p>
          <p className="text-xs text-green-600 mt-1">↑ 12% from last month</p>
        </div>

        <div className="bg-card p-6 rounded-lg border border-border shadow-sm">
          <p className="text-sm text-muted-foreground mb-1">Total Bookings</p>
          <p className="text-2xl font-bold text-primary">142</p>
          <p className="text-xs text-green-600 mt-1">↑ 8% from last month</p>
        </div>

        <div className="bg-card p-6 rounded-lg border border-border shadow-sm">
          <p className="text-sm text-muted-foreground mb-1">Active Clients</p>
          <p className="text-2xl font-bold text-primary">89</p>
          <p className="text-xs text-blue-600 mt-1">↑ 5% from last month</p>
        </div>

        <div className="bg-card p-6 rounded-lg border border-border shadow-sm">
          <p className="text-sm text-muted-foreground mb-1">Pending Bookings</p>
          <p className="text-2xl font-bold text-orange-600">12</p>
          <p className="text-xs text-orange-600 mt-1">Needs attention</p>
        </div>
      </div>

      {/* Chart */}
      <div className="bg-card p-6 rounded-lg border border-border shadow-sm">
        <h2 className="text-lg font-semibold mb-4">Revenue & Bookings</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="revenue" fill="#3b82f6" />
            <Bar dataKey="bookings" fill="#10b981" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-card p-6 rounded-lg border border-border shadow-sm">
          <h2 className="text-lg font-semibold mb-4">Recent Bookings</h2>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center justify-between p-3 bg-accent/5 rounded-md">
                <div>
                  <p className="font-medium text-sm">Booking #BK{String(i).padStart(8, '0')}</p>
                  <p className="text-xs text-muted-foreground">John Doe • 2 days ago</p>
                </div>
                <span className="text-xs font-semibold text-green-600">Confirmed</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-card p-6 rounded-lg border border-border shadow-sm">
          <h2 className="text-lg font-semibold mb-4">Top Packages</h2>
          <div className="space-y-3">
            {['Paris Adventure', 'Tokyo Experience', 'Dubai Luxury'].map((pkg, i) => (
              <div key={i} className="flex items-center justify-between p-3 bg-accent/5 rounded-md">
                <div>
                  <p className="font-medium text-sm">{pkg}</p>
                  <p className="text-xs text-muted-foreground">{12 + i} bookings this month</p>
                </div>
                <span className="text-xs font-semibold text-primary">${1200 + i * 100}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
