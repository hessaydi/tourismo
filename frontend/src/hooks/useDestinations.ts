import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/services/api';
import { Destination } from '@/types';

// Query keys
export const destinationKeys = {
  all: ['destinations'] as const,
  lists: () => [...destinationKeys.all, 'list'] as const,
  list: (filters: Record<string, unknown>) => [...destinationKeys.lists(), { filters }] as const,
  details: () => [...destinationKeys.all, 'detail'] as const,
  detail: (id: number) => [...destinationKeys.details(), id] as const,
};

// Queries
export const useDestinations = (skip = 0, limit = 100) => {
  return useQuery({
    queryKey: destinationKeys.list({ skip, limit }),
    queryFn: async () => {
      const response = await apiClient.get('/destinations', {
        params: { skip, limit },
      });
      return response.data;
    },
  });
};

export const useDestination = (id: number) => {
  return useQuery({
    queryKey: destinationKeys.detail(id),
    queryFn: async () => {
      const response = await apiClient.get(`/destinations/${id}`);
      return response.data;
    },
  });
};

// Mutations
export const useCreateDestination = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: Partial<Destination>) => {
      const response = await apiClient.post('/destinations', data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: destinationKeys.lists() });
    },
  });
};

export const useUpdateDestination = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<Destination> }) => {
      const response = await apiClient.put(`/destinations/${id}`, data);
      return response.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: destinationKeys.lists() });
      queryClient.invalidateQueries({ queryKey: destinationKeys.detail(data.id) });
    },
  });
};

export const useDeleteDestination = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/destinations/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: destinationKeys.lists() });
    },
  });
};
