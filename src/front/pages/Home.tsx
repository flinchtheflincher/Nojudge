import React from 'react';
import { useCompanion } from '../../hooks/useCompanion';
import { CompanionFigure } from '../../components/Companion/CompanionFigure';
import { CompanionChat } from '../../components/Companion/CompanionChat';
import { useNavigate } from 'react-router-dom';
import './Home.css';

export const Home: React.FC = () => {
    const { companion, messages, loading, error, sendMessage } = useCompanion();
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
    };

    if (loading && !companion) {
        return (
            <div className="home-loading">
                <div className="spinner"></div>
                <p>Loading your companion...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="home-error">
                <h2>Error</h2>
                <p>{error}</p>
                <button onClick={handleLogout} className="btn btn-primary">
                    Back to Login
                </button>
            </div>
        );
    }

    return (
        <div className="home-container">
            <header className="home-header">
                <div className="header-content">
                    <h2>Nojudge</h2>
                    <button onClick={handleLogout} className="btn btn-secondary">
                        Logout
                    </button>
                </div>
            </header>

            <div className="home-content">
                <div className="companion-section">
                    <CompanionFigure companion={companion} />
                </div>

                <div className="chat-section">
                    <div className="chat-wrapper">
                        <h3 className="chat-title">Chat with {companion?.name}</h3>
                        <p className="chat-subtitle">
                            Personality: {companion?.personality_type}
                        </p>
                        <CompanionChat
                            messages={messages}
                            onSendMessage={sendMessage}
                            isLoading={loading}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};
