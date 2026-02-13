import React, { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { CompanionState } from '../../hooks/useCompanion';
import '../../styles/companion.css';

interface CompanionFigureProps {
    companion: CompanionState | null;
}

export const CompanionFigure: React.FC<CompanionFigureProps> = ({ companion }) => {
    const headRef = useRef<HTMLDivElement>(null);
    const bodyRef = useRef<HTMLDivElement>(null);
    const figureRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!headRef.current || !bodyRef.current || !figureRef.current) return;

        // Idle breathing animation
        gsap.to(headRef.current, {
            scale: 1.05,
            duration: 2,
            yoyo: true,
            repeat: -1,
            ease: 'sine.inOut',
        });

        gsap.to(bodyRef.current, {
            scaleY: 1.03,
            scaleX: 1.01,
            duration: 2.5,
            yoyo: true,
            repeat: -1,
            ease: 'sine.inOut',
            delay: 0.2,
        });

        // Mouse parallax effect
        const handleMouseMove = (e: MouseEvent) => {
            const xPos = e.clientX / window.innerWidth - 0.5;
            const yPos = e.clientY / window.innerHeight - 0.5;

            gsap.to(headRef.current, {
                x: xPos * 40,
                y: yPos * 30,
                rotationY: xPos * 30,
                rotationX: -yPos * 20,
                duration: 0.8,
                ease: 'power2.out',
            });

            gsap.to(bodyRef.current, {
                x: xPos * 20,
                y: yPos * 15,
                rotationY: xPos * 10,
                rotationX: -yPos * 10,
                duration: 0.8,
                ease: 'power2.out',
            });

            gsap.to(figureRef.current, {
                rotationZ: xPos * 5,
                duration: 1,
                ease: 'power1.out',
            });
        };

        window.addEventListener('mousemove', handleMouseMove);

        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    // Activity-specific animations
    useEffect(() => {
        if (!companion || !headRef.current || !bodyRef.current) return;

        const activity = companion.current_activity;

        // Reset to default state first
        gsap.killTweensOf([headRef.current, bodyRef.current]);

        // Restart breathing animation
        gsap.to(headRef.current, {
            scale: 1.05,
            duration: 2,
            yoyo: true,
            repeat: -1,
            ease: 'sine.inOut',
        });

        gsap.to(bodyRef.current, {
            scaleY: 1.03,
            scaleX: 1.01,
            duration: 2.5,
            yoyo: true,
            repeat: -1,
            ease: 'sine.inOut',
            delay: 0.2,
        });

        // Activity-specific animations
        if (activity === 'cooking') {
            // Slight bouncing motion
            gsap.to(bodyRef.current, {
                y: '+=10',
                duration: 0.5,
                yoyo: true,
                repeat: 5,
                ease: 'power1.inOut',
            });
        } else if (activity === 'eating') {
            // Gentle swaying
            gsap.to(headRef.current, {
                rotation: 5,
                duration: 1,
                yoyo: true,
                repeat: 3,
                ease: 'sine.inOut',
            });
        } else if (activity === 'sleeping') {
            // Slow, deep breathing
            gsap.to(bodyRef.current, {
                scaleY: 1.05,
                duration: 3,
                yoyo: true,
                repeat: -1,
                ease: 'sine.inOut',
            });
        } else if (activity === 'exploring') {
            // Quick head movements
            gsap.to(headRef.current, {
                x: '+=20',
                duration: 0.3,
                yoyo: true,
                repeat: 6,
                ease: 'power2.inOut',
            });
        }
    }, [companion?.current_activity]);

    if (!companion) {
        return (
            <div className="companion-figure-wrapper">
                <div className="spinner"></div>
            </div>
        );
    }

    return (
        <div className="companion-container">
            <div className="companion-status">
                <h1 className="companion-name">{companion.name}</h1>
                <div className="companion-activity">{companion.current_activity}</div>
            </div>

            <div
                className="companion-figure-wrapper"
                ref={figureRef}
                data-activity={companion.current_activity}
            >
                <div className="companion-head" ref={headRef}></div>
                <div className="companion-body" ref={bodyRef}></div>
            </div>

            <div className="companion-stats">
                <div className="stat-bar">
                    <span className="stat-label">Mood</span>
                    <div className="stat-progress">
                        <div
                            className="stat-fill mood"
                            style={{ width: `${companion.mood}%` }}
                        ></div>
                    </div>
                </div>
                <div className="stat-bar">
                    <span className="stat-label">Energy</span>
                    <div className="stat-progress">
                        <div
                            className="stat-fill energy"
                            style={{ width: `${companion.energy_level}%` }}
                        ></div>
                    </div>
                </div>
            </div>
        </div>
    );
};
