# Tourismo Frontend

A modern, responsive React + TypeScript + Vite frontend for the Tourismo Travel Agency Management System with shadcn/ui components and Tailwind CSS.

## 🚀 Features

- **React 18 + TypeScript**: Type-safe component development
- **Vite**: Lightning-fast build tool and development server
- **shadcn/ui**: High-quality, accessible React components
- **Tailwind CSS**: Utility-first CSS framework
- **React Router v6**: Client-side routing
- **TanStack Query**: Powerful data synchronization library
- **Dark/Light Mode**: Theme switching support
- **Responsive Design**: Mobile-first, fully responsive UI
- **JWT Authentication**: Secure token-based auth
- **RBAC**: Role-based access control

## 📋 Project Structure

```
src/
├── components/          # Reusable UI components
│   └── ui/             # shadcn/ui components
├── contexts/           # React contexts (Auth, Theme)
├── hooks/              # Custom React hooks
├── layouts/            # Layout components
├── pages/              # Page components
│   ├── auth/
│   ├── dashboard/
│   ├── packages/
│   ├── clients/
│   ├── bookings/
│   ├── destinations/
│   └── guides/
├── services/           # API services
├── types/              # TypeScript types
├── utils/              # Utility functions
├── App.tsx             # Main App component
├── main.tsx            # Entry point
└── index.css           # Global styles
```

## 🛠️ Installation

### Prerequisites
- Node.js 16+
- npm or yarn or pnpm

### Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env.local
   ```

3. **Configure API URL** (edit `.env.local`)
   ```
   VITE_API_URL=http://localhost:8000
   ```

## 🚀 Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## 📦 Building

Build for production:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## 🧪 Type Checking

Run TypeScript type checking:
```bash
npm run type-check
```

## 📚 Architecture

### Authentication Flow
1. User logs in with username/password
2. Backend returns `access_token` and `refresh_token`
3. Tokens are stored in `localStorage`
4. Axios interceptor adds token to all requests
5. On 401, token is automatically refreshed

### State Management
- **Local State**: React `useState` for component-level state
- **Server State**: TanStack Query for API data caching
- **Global State**: React Context (Auth, Theme)

### Component Architecture
- **Layout Components**: `MainLayout`, `AuthLayout`
- **UI Components**: Reusable styled components from shadcn/ui
- **Page Components**: Full-page screens
- **Feature Components**: Business logic components

## 🎨 Theme Customization

Dark and light mode is supported via CSS variables. Theme colors are defined in `tailwind.config.ts`:

```ts
colors: {
  primary: "hsl(var(--primary))",
  secondary: "hsl(var(--secondary))",
  // ...
}
```

Customize in `src/index.css`:

```css
:root {
  --primary: 221.2 83.2% 53.3%;
  --secondary: ...
}
```

## 🔐 Security

- Passwords are never stored locally
- JWT tokens stored in `localStorage`
- HTTPS recommended for production
- CORS properly configured
- Input validation with React Hook Form

## 🐳 Docker

Build Docker image:
```bash
docker build -t tourismo-frontend .
docker run -p 5173:5173 tourismo-frontend
```

## 📄 API Integration

All API calls go through `apiClient` in `src/services/api.ts`:

```ts
import { apiClient } from '@/services/api';

const response = await apiClient.get('/destinations');
```

TanStack Query hooks provide automatic caching:

```ts
import { useDestinations } from '@/hooks/useDestinations';

const { data, isLoading, error } = useDestinations();
```

## 🚀 Performance Optimizations

- Code splitting with React Router
- Image optimization
- CSS-in-JS efficient bundling
- Lazy loading of routes
- Query caching with TanStack Query

## 📝 Common Tasks

### Add a new page
1. Create `src/pages/feature/FeaturePage.tsx`
2. Add route in `App.tsx`
3. Add navigation in `Sidebar.tsx`

### Add a new component
1. Create `src/components/Feature.tsx`
2. Import and use in pages

### Add API integration
1. Create hook in `src/hooks/useFeature.ts`
2. Use `apiClient` for requests
3. Export hooks for use in components

## 🔗 Useful Links

- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [React Router Documentation](https://reactrouter.com)
- [TanStack Query Documentation](https://tanstack.com/query)

## 📄 License

This project is part of the Tourismo Travel Agency Management System.

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📞 Support

For issues and questions, please open an issue in the repository.
