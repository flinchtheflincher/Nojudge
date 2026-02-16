# Project Description: Nojudge

**Project Name:** Nojudge

**One-Line Pitch:**
An autonomous AI companion platform providing judgment-free emotional support through interactive 3D avatars and evolving personalities.

**Detailed Description:**
Nojudge is a full-stack web application designed to combat loneliness and support mental wellness. It provides users with an "always-there" digital companion that possesses its own distinct personality, emotional state, and autonomous behaviors. Unlike passive chatbots, Nojudge companions initiate interactions, perform daily activities (like cooking or reading), and react dynamically to the user's mood, creating a sense of genuine presence and connection.

**Technical Architecture & AWS Utilization:**
Currently built with React/TypeScript (frontend) and Python/Flask (backend), we are moving to a cloud-native architecture to scale.
*   **Compute:** We will use **Amazon EC2** and **Auto Scaling** groups to handle real-time WebSocket connections for live companion updates.
*   **Database:** We are migrating our state management to **Amazon RDS (PostgreSQL)** to ensure data integrity for long-term user-companion memory.
*   **Storage:** **Amazon S3** will host the 3D assets and user-generated customization files, delivered via **Amazon CloudFront** for low latency.
*   **AI/ML:** The core innovation lies in our personality engine. We plan to use **Amazon SageMaker** to fine-tune models that can maintain consistent personality traits over long conversations, distinguishing our product from generic LLM wrappers.

The requested AWS credits will be critical for this migration, allowing us to stress-test our real-time infrastructure and train our improving personality models without prohibitive upfront costs.
