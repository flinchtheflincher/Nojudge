import React, { useState, useRef, useEffect } from 'react';
import { Message } from '../../hooks/useCompanion';
import './CompanionChat.css';

interface CompanionChatProps {
    messages: Message[];
    onSendMessage: (message: string) => Promise<string>;
    isLoading?: boolean;
}

export const CompanionChat: React.FC<CompanionChatProps> = ({
    messages,
    onSendMessage,
    isLoading = false,
}) => {
    const [inputValue, setInputValue] = useState('');
    const [sending, setSending] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!inputValue.trim() || sending) return;

        const message = inputValue.trim();
        setInputValue('');
        setSending(true);

        try {
            await onSendMessage(message);
        } catch (error) {
            console.error('Failed to send message:', error);
        } finally {
            setSending(false);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-messages">
                {messages.length === 0 ? (
                    <div className="chat-empty">
                        <p>Start a conversation with your companion!</p>
                    </div>
                ) : (
                    messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={`message ${msg.is_user_message ? 'user' : 'companion'}`}
                        >
                            <div className="message-content">{msg.content}</div>
                            <div className="message-time">
                                {new Date(msg.created_at).toLocaleTimeString([], {
                                    hour: '2-digit',
                                    minute: '2-digit',
                                })}
                            </div>
                        </div>
                    ))
                )}
                {sending && (
                    <div className="message companion typing">
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form className="chat-input-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Type a message..."
                    disabled={sending}
                    className="chat-input"
                />
                <button
                    type="submit"
                    disabled={!inputValue.trim() || sending}
                    className="btn btn-primary chat-send-btn"
                >
                    Send
                </button>
            </form>
        </div>
    );
};
