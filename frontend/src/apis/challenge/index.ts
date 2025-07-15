import { useApi } from "@/hooks/useApi.ts";

interface GenerateChallengeData {
    difficulty: string;
    title?: string;
    options?: string[];
    correct_answer_id?: number;
    explanation?: string;
}

export const generateChallenge: (data: GenerateChallengeData) => Promise<void>
    = async (data: GenerateChallengeData): Promise<void> => {
    const endpoint = '/api/challenge/generate-challenge';
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    };
    return useApi()(endpoint, options);
};

export const getHistory: () => Promise<void> = async (): Promise<void> => {
    const endpoint = '/api/history';
    const options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    };
    return useApi()(endpoint, options);
};

export const getQuote: () => Promise<void> = async (): Promise<void> => {
    const endpoint = '/api/quote';
    const options = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    };
    return useApi()(endpoint, options);
};