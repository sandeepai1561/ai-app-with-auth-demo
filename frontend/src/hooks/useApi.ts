import {useAuth} from "@clerk/clerk-react";

interface RequestInit {
    method?: string;
    headers?: Record<string, string>;
    body?: any;
}

const API_URL = import.meta.env.VITE_API_URL;

export const useApi: () => (endpoint: string, options?: RequestInit) => Promise<void>
    = (): ((endpoint: string, options?: RequestInit) => Promise<void>) => {
    const { getToken } = useAuth();
    const makeRequest: (endpoint: string, options: RequestInit) => Promise<void> = async (
        endpoint: string,
        options: RequestInit = {}
    ): Promise<void> => {
        const token: string | null = await getToken();
        const response: Response = await fetch(`${API_URL}/${endpoint}`, {
            ...options,
            headers: {
                ...options.headers,
                Authorization: `Bearer ${token}`,
            },
        });
        if (!response.ok) {
            const error = await response.json()
                .catch(() => null)
            if (error.status === 401 && error.message === 'Unauthorized') {
                throw new Error('Unauthorized');
            }
            if (error.status === 403 && error.message === 'Forbidden') {
                throw new Error('Forbidden');
            }
            if (error.status === 404 && error.message === 'Not Found') {
                throw new Error('Not Found');
            }
            if (error.status === 429 && error.message === 'Too Many Requests') {
                throw new Error('Too Many Requests');
            }
            if (error.status === 500 && error.message === 'Internal Server Error') {
                throw new Error('Internal Server Error');
            }
        }
        return response.json();
    }
    return makeRequest as (endpoint: string, options?: RequestInit) => Promise<void>;
}
