// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {
    // User's previous code (preserved)
    // const addCamera = Document.getE 

    const head = document.getElementById("head");
    const body = document.getElementById("body");
    const figure = document.getElementById("figure");

    if (!head || !body || !figure) return;

    // 1. Idle "Breathing" Animation
    gsap.to(head, {
        scale: 1.05,
        duration: 2,
        yoyo: true,
        repeat: -1,
        ease: "sine.inOut"
    });

    gsap.to(body, {
        scaleY: 1.03,
        scaleX: 1.01,
        duration: 2.5,
        yoyo: true,
        repeat: -1,
        ease: "sine.inOut",
        delay: 0.2
    });

    // 2. Interactive "Look" / Parallax Effect
    window.addEventListener("mousemove", (e) => {
        const xPos = (e.clientX / window.innerWidth - 0.5);
        const yPos = (e.clientY / window.innerHeight - 0.5);

        gsap.to(head, {
            x: xPos * 40,
            y: yPos * 30,
            rotationY: xPos * 30,
            rotationX: -yPos * 20,
            duration: 0.8,
            ease: "power2.out"
        });

        gsap.to(body, {
            x: xPos * 20,
            y: yPos * 15,
            rotationY: xPos * 10,
            rotationX: -yPos * 10,
            duration: 0.8,
            ease: "power2.out"
        });

        gsap.to(figure, {
            rotationZ: xPos * 5,
            duration: 1,
            ease: "power1.out"
        });
    });
});