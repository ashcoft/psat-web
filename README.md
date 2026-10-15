# PSAT Web - Power System Analysis Toolbox

A modern web-based power system analysis and simulation tool, ported from the original MATLAB-based PSAT.

![PSAT Web](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)
![React](https://img.shields.io/badge/React-18.3.1-61dafb.svg)
![Next.js](https://img.shields.io/badge/Next.js-14.2.35-000000.svg)

## Features

### Power System Analysis
- **Power Flow Analysis**: Newton-Raphson, DC, and Fast Decoupled methods
- **Time Domain Simulation**: Dynamic simulation of power system behavior
- **Eigenvalue Analysis**: Small-signal stability assessment
- **Continuation Power Flow**: Voltage stability analysis

### Visualization
- **Interactive Canvas**: Drag-and-drop component placement
- **Real-time Results**: Voltage, angle, and loading visualization
- **Zoom and Pan**: Navigate large power systems easily

### UI/UX
- **Ribbon Interface**: Similar to Microsoft Word/Etap for familiar experience
- **Component Browser**: Sidebar for quick component insertion
- **Properties Panel**: Detailed view of selected components
- **Output Window**: Real-time analysis results and logs

## Tech Stack

- **Frontend**: React 18 with TypeScript
- **Framework**: Next.js 14
- **Styling**: Tailwind CSS
- **Visualization**: HTML5 Canvas
- **Containerization**: Docker & Docker Compose

## Getting Started

### Prerequisites

- Node.js 18+
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/psat-web.git
cd psat-web

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

### Docker Deployment

```bash
# Build Docker image
docker build -t psat-web .

# Run with Docker Compose
docker-compose up -d

# Or run directly
docker run -p 3000:3000 psat-web
```

## Architecture

```
src/
├── app/           # Next.js App Router pages
├── components/     # React UI components
│   ├── Canvas.tsx       # Power system visualization
│   ├── Ribbon.tsx       # Microsoft-style ribbon menu
│   ├── Sidebar.tsx      # Component browser
│   ├── Toolbar.tsx      # Quick action toolbar
│   ├── PropertiesPanel  # Component properties editor
│   └── OutputWindow     # Analysis results display
├── lib/           # Core algorithms
│   └── powerflow.ts     # Power flow solver
└── types/         # TypeScript definitions
    └── index.ts         # System data structures
```

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm run release` | Run a release locally with semantic-release (normally done by CI) |

## Releases

Releases are automated with [semantic-release](https://github.com/semantic-release/semantic-release) and driven by [Conventional Commits](https://www.conventionalcommits.org/).

The `Release` workflow (`.github/workflows/release.yml`) runs on every push to `main` and can also be started manually. It:

1. analyses the commits since the last release to work out the next version,
2. updates `package.json`/`package-lock.json`, writes `CHANGELOG.md` and commits them back to `main`,
3. creates the Git tag and the GitHub Release with generated release notes.

Commit messages therefore determine the version bump:

| Commit message | Release |
|----------------|---------|
| `fix: ...` | patch (`1.0.0` → `1.0.1`) |
| `feat: ...` | minor (`1.0.0` → `1.1.0`) |
| `feat!: ...` or `BREAKING CHANGE:` in the body | major (`1.0.0` → `2.0.0`) |
| `chore: ...`, `docs: ...`, `test: ...`, `ci: ...` | no release |

The configuration lives in `.releaserc.json`. Publishing to the npm registry is disabled (`npmPublish: false`) — this project is an application, not a library.

## Power Flow Solver

The application includes a Newton-Raphson power flow solver with:

- Y-Bus matrix construction
- Power mismatch calculation
- Voltage initialization (flat start supported)
- Convergence checking
- Line loading calculation
- System losses computation

## Containerized Deployment

The application is fully containerized for easy deployment:

```yaml
# docker-compose.yml
services:
  psat-web:
    build: .
    ports:
      - "3000:3000"
    restart: unless-stopped
```

## Original PSAT

This project is a web-based port of the original [PSAT - Power System Analysis Toolbox](https://faraday1.ucd.ie/psat.html) developed by Federico Milano.

Original PSAT is:
- Copyright (C) 2002-2016 Federico Milano
- Free software under GNU General Public License v3

## License

This project maintains compatibility with the original GPL-3.0 license. See LICENSE file for details.

## Contributing

Contributions are welcome! Please read the contribution guidelines before submitting PRs.

## Acknowledgments

- Original PSAT by Federico Milano
- Power system analysis algorithms from academic literature# Web Version
