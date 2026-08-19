// API response types
export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  role: 'admin' | 'manager' | 'user';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface Destination {
  id: number;
  name: string;
  country: string;
  description: string;
  image_url?: string;
  is_featured: boolean;
  created_at: string;
}

export interface Package {
  id: number;
  title: string;
  destination_id: number;
  category: string;
  description: string;
  duration_days: number;
  price_per_person: number;
  max_capacity: number;
  status: string;
  includes?: string;
  image_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Client {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  passport_number?: string;
  nationality?: string;
  date_of_birth?: string;
  address?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface Booking {
  id: number;
  booking_ref: string;
  client_id: number;
  package_id: number;
  travel_date: string;
  return_date: string;
  num_travelers: number;
  total_price: number;
  status: string;
  payment_status: string;
  special_requests?: string;
  created_at: string;
  updated_at: string;
}

export interface Guide {
  id: number;
  name: string;
  email: string;
  phone: string;
  languages: string;
  specialties?: string;
  bio?: string;
  rating: number;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message?: string;
  link?: string;
  is_read: boolean;
  created_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}
