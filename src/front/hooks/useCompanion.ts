import { useState, useEffect, useCallback } from 'react';
import { companionAPI } from '../utils/api';
import { io, Socket } from 'socket.io-client';

export interface CompanionState {
    id: number;
    user_id: number;
    name: string;
    personality_type: string;
    personality_description: string;
    current_activity: string;
    mood: number;
    energy_level: number;
    last_activity_time: string;
    created_at: string;
}

export interface Message {
    id: number;
    companion_id: number;
    is_user_message: boolean;
    content: string;
    created_at: string;
}

const SOCKET_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

export const useCompanion = () => {
    const [companion, setCompanion] = useState<CompanionState | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [socket, setSocket] = useState<Socket | null>(null);

    // Initialize socket connection
    useEffect(() => {
        const newSocket = io(SOCKET_URL);
        setSocket(newSocket);

        newSocket.on('connected', (data) => {
            console.log('Connected to server:', data.message);
        });

        newSocket.on('activity_changed', (data) => {
            console.log('Activity changed:', data);
            setCompanion(data.companion_state);
        });

        newSocket.on('activity_update', (data) => {
            setCompanion(data.companion_state);
        });

        return () => {
            newSocket.close();
        };
    }, []);

    // Fetch companion state
    const fetchCompanion = useCallback(async () => {
        try {
            setLoading(true);
            const response = await companionAPI.getCompanion();
            setCompanion(response.data);
            setError(null);
        } catch (err: any) {
            setError(err.response?.data?.error || 'Failed to fetch companion');
        } finally {
            setLoading(false);
        }
    }, []);

    // Fetch conversation history
    const fetchHistory = useCallback(async () => {
        try {
            const response = await companionAPI.getHistory();
            setMessages(response.data.messages);
        } catch (err: any) {
            console.error('Failed to fetch history:', err);
        }
    }, []);

    // Send message to companion
    const sendMessage = useCallback(async (message: string) => {
        try {
            const response = await companionAPI.sendMessage(message);

            // Add both messages to the list
            setMessages(prev => [
                ...prev,
                response.data.user_message,
                response.data.companion_message
            ]);

            // Update companion state
            setCompanion(response.data.companion_state);

            return response.data.companion_message.content;
        } catch (err: any) {
            throw new Error(err.response?.data?.error || 'Failed to send message');
        }
    }, []);

    // Request activity update via socket
    const requestActivityUpdate = useCallback(() => {
        if (socket && companion) {
            socket.emit('request_activity_update', { user_id: companion.user_id });
        }
    }, [socket, companion]);

    // Initial fetch
    useEffect(() => {
        fetchCompanion();
        fetchHistory();
    }, [fetchCompanion, fetchHistory]);

    // Poll for activity updates every 30 seconds
    useEffect(() => {
        const interval = setInterval(() => {
            requestActivityUpdate();
        }, 30000);

        return () => clearInterval(interval);
    }, [requestActivityUpdate]);

    return {
        companion,
        messages,
        loading,
        error,
        sendMessage,
        fetchCompanion,
        requestActivityUpdate,
    };
};
