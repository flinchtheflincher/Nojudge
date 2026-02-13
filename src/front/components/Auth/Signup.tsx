import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../../utils/api';
import './Auth.css';

const PERSONALITIES = [
    { value: 'intelligent', label: 'Intelligent', description: 'Smart and analytical' },
    { value: 'lazy', label: 'Lazy', description: 'Relaxed and easygoing' },
    { value: 'inquisitive', label: 'Inquisitive', description: 'Curious and questioning' },
    { value: 'cheerful', label: 'Cheerful', description: 'Happy and optimistic' },
    { value: 'grumpy', label: 'Grumpy', description: 'A bit cranky but lovable' },
    { value: 'curious', label: 'Curious', description: 'Interested in everything' },
];

export const Signup: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [personality, setPersonality] = useState('curious');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        // Validation
        if (password.length < 6) {
            setError('Password must be at least 6 characters');
            return;
        }

        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        setLoading(true);

        try {
            const response = await authAPI.signup(email, password, personality);
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
            navigate('/');
        } catch (err: any) {
            setError(err.response?.data?.error || 'Signup failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card glass">
                <h1 className="auth-title">Create Your Companion</h1>
                <p className="auth-subtitle">Choose a personality and get started</p>

                {error && <div className="auth-error">{error}</div>}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input
                            type="email"
                            id="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="your@email.com"
                            required
                            autoComplete="email"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                            required
                            autoComplete="new-password"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="confirmPassword">Confirm Password</label>
                        <input
                            type="password"
                            id="confirmPassword"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="••••••••"
                            required
                            autoComplete="new-password"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="personality">Companion Personality</label>
                        <select
                            id="personality"
                            value={personality}
                            onChange={(e) => setPersonality(e.target.value)}
                            className="personality-select"
                        >
                            {PERSONALITIES.map((p) => (
                                <option key={p.value} value={p.value}>
                                    {p.label} - {p.description}
                                </option>
                            ))}
                        </select>
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary w-full"
                        disabled={loading}
                    >
                        {loading ? 'Creating...' : 'Create Account'}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>
                        Already have an account?{' '}
                        <Link to="/login" className="auth-link">
                            Sign in
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
};
