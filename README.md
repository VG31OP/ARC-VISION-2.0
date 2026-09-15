# ARC VISION — Intelligent Surveillance Platform

> **“See More. Know Faster. Act Smarter.”**

ARC VISION is an enterprise-grade intelligent surveillance and real-time NVR platform engineered for high-performance security command centers, incident response, evidence preservation, and proactive threat detection.

---

## Overview

ARC VISION combines modern command-center user experience with hardware-accelerated computer vision, ultra-low latency live streaming, and automated incident intelligence. It runs locally with minimal resource footprint and maximum efficiency.

### Core Capabilities

- **Live Surveillance UX**: Multi-camera grid layouts, responsive streams powered by WebRTC / MSE, PTZ controls, and dynamic stream selection.
- **Incident Intelligence**: Real-time object detection and tracking (persons, vehicles, animals, packages), classification, and automated alert scoring.
- **Security Zones & Spatial Boundaries**: Interactive in-browser zone and mask editors for perimeter monitoring, loitering alerts, and speed estimation.
- **Evidence Workflow**: Synchronized recording playback, high-resolution incident snapshots, incident clips, and full export capabilities.
- **Enrichments**: Built-in face recognition, license plate recognition (LPR), semantic search, and generative AI incident summaries.
- **Alert Operations**: Incident change feeds, severity triage, instant notifications via WebPush and MQTT.
- **Analytics & System Health**: Real-time monitoring of CPU/GPU utilization, detector latency, camera frame rates, and storage pools.
- **Access Control & Security**: Multi-user role-based access (admin vs viewer), session tokens, and TLS termination.

---

## Architecture Overview

```text
                                  ┌───────────────────────────┐
                                  │   IP Cameras / MediaMTX   │
                                  └─────────────┬─────────────┘
                                                │ RTSP / WebRTC
                                                ▼
                                  ┌───────────────────────────┐
                                  │  go2rtc / FFmpeg Capture  │
                                  └─────────────┬─────────────┘
                                                │ Frame Buffers (SHM)
                                                ▼
┌──────────────────────────┐      ┌───────────────────────────┐      ┌──────────────────────────┐
│ Object & Audio Detectors │ ◄──► │  ARC VISION Vision Engine │ ◄──► │  Enrichments (LPR/Face)  │
└──────────────────────────┘      └─────────────┬─────────────┘      └──────────────────────────┘
                                                │ ZMQ / Async Events
                                                ▼
                                  ┌───────────────────────────┐
                                  │ FastAPI Backend & DB      │
                                  └─────────────┬─────────────┘
                                                │ REST / WebSockets / MQTT
                                                ▼
                                  ┌───────────────────────────┐
                                  │ ARC VISION Command Center │
                                  │      (React + Vite)       │
                                  └───────────────────────────┘
```

---

## Getting Started

### 1. Prerequisites

- **Docker & Docker Compose** (or native Linux environment)
- **RTSP-capable IP Cameras** or simulated video streams
- **Supported Accelerator** (optional but recommended: Google Coral EdgeTPU, Intel/AMD GPU, Nvidia GPU with TensorRT, OpenVINO, Apple Silicon, Rockchip RKNN, or Hailo-8L)

### 2. Deployment with Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: "3.9"
services:
  arc-vision:
    container_name: arc-vision
    privileged: true
    restart: unless-stopped
    image: ghcr.io/arc-vision/arc-vision:stable
    shm_size: "128mb" # Adjust according to camera resolution
    devices:
      - /dev/dri/renderD128 # Hardware acceleration device (if available)
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./config:/config
      - ./storage:/media/frigate
      - type: tmpfs # Optional: 1GB of memory, reduces SSD wear
        target: /tmp/cache
        tmpfs:
          size: 1000000000
    ports:
      - "8971:8971" # Authenticated WebUI / API
      - "5000:5000" # Internal unauthenticated WebUI (optional)
      - "8554:8554" # RTSP restream
      - "8555:8555/tcp" # WebRTC
      - "8555:8555/udp" # WebRTC
    environment:
      FRIGATE_RTSP_PASSWORD: "your_camera_password"
```

### 3. Configuration (`config/config.yml`)

```yaml
mqtt:
  enabled: true
  host: mqtt.local
  topic_prefix: frigate

cameras:
  front_door:
    ffmpeg:
      inputs:
        - path: rtsp://viewer:{FRIGATE_RTSP_PASSWORD}@192.168.1.100:554/live
          roles:
            - detect
            - record
    detect:
      width: 1280
      height: 720
      fps: 5
    record:
      enabled: true
      retain:
        days: 7
        mode: all
    snapshots:
      enabled: true

detectors:
  cpu1:
    type: cpu
```

---

## Key Modules & Terminology

| Concept | ARC VISION Term | Description |
| :--- | :--- | :--- |
| **Live Streams** | **Live Surveillance** | Sub-second video monitoring with multi-grid dashboards and PTZ |
| **Detection Events** | **Incidents** | Classified and tracked security occurrences with confidence scoring |
| **Event Timeline** | **Incident Review** | Multi-camera correlated incident feeds with preview cards |
| **Video Archives** | **Evidence** | Retained continuous or motion-triggered video recordings |
| **Clips & Stills** | **Incident Snapshots & Clips** | Clean and annotated evidence artifacts with metadata |
| **Detection Areas** | **Security Zones** | User-defined polygons for entering/exiting alerts and loitering tracking |
| **Metrics & Health** | **Analytics & System Health** | Live metrics for FPS, inference speeds, CPU/GPU, and storage health |

---

## Integrations

- **Home Assistant**: Full two-way integration with auto-discovered cameras, incident sensors, notification blueprints, and switches.
- **MQTT**: Real-time event broadcasts, incident status updates, PTZ control, and state management.
- **HomeKit**: Direct live camera feed and two-way talk streaming via go2rtc.
- **REST & WebSocket API**: Comprehensive API for security operations and automation tools.

---

## Development & Testing

```bash
# Backend unit tests
python3 -u -m unittest

# Code formatting & linting
ruff format frigate/
ruff check frigate/

# Frontend (from web/ directory)
npm install
npm run build
npm run lint
```

---

## Open Source Attribution & Licensing

ARC VISION is built upon and acknowledges foundational open-source technologies including OpenCV, TensorFlow/ONNX, FastAPI, and go2rtc.

- **License**: Distributed under the [MIT License](LICENSE).
- **Notices**: Detailed third-party credits and attribution are maintained in [ARC_VISION_OPEN_SOURCE_NOTICES.md](ARC_VISION_OPEN_SOURCE_NOTICES.md).
