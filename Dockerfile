# Use Node.js LTS as base image
FROM node:20-alpine AS base

# Install dependencies stage
FROM base AS deps

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Build stage
FROM deps AS builder

WORKDIR /app

# Copy all source files
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM base AS runner

WORKDIR /app

# Set environment for production
ENV NODE_ENV=production

# Create non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public

# Set ownership
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Start the application
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["npm", "start"]