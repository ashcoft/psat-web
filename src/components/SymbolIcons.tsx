/**
 * PSAT/IEEE Standard SVG Icons for Power System Components
 * Based on PSAT single-line diagram symbols and IEEE/IEC standards
 */

import React from 'react';

interface IconProps {
  size?: number;
  className?: string;
}

const SvgWrapper: React.FC<{
  children: React.ReactNode;
  size?: number;
  className?: string;
  viewBox?: string;
}> = ({
  children,
  size = 24,
  className = '',
  viewBox = '0 0 24 24',
}) => (
  <svg
    width={size}
    height={size}
    viewBox={viewBox}
    className={className}
    fill="none"
    stroke="currentColor"
    strokeWidth="1.8"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {children}
  </svg>
);

// ===================== BUSES =====================

/** Slack/Infinite Bus */
export const SlackBusIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="14" x2="22" y2="14" strokeWidth="3" />
    <line x1="2" y1="14" x2="7" y2="7" />
    <line x1="2" y1="14" x2="7" y2="21" />
  </SvgWrapper>
);

/** PV Bus */
export const PVBusIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="14" x2="22" y2="14" strokeWidth="3" />
    <circle cx="12" cy="14" r="4" fill="none" />
  </SvgWrapper>
);

/** PQ Bus */
export const PQBusIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="14" x2="22" y2="14" strokeWidth="3" />
    <circle cx="12" cy="14" r="2" fill="currentColor" />
  </SvgWrapper>
);

// ===================== GENERATION =====================

/** Generator: circle with G inside */
export const GeneratorIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="10" fill="none" />
    <text x="12" y="16" textAnchor="middle" fontSize="14" fontWeight="bold" fill="currentColor" stroke="none">
      G
    </text>
  </SvgWrapper>
);

/** External Grid: circle with cross */
export const ExternalGridIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <circle cx="12" cy="11" r="9" fill="none" />
    <line x1="12" y1="2" x2="12" y2="20" />
    <line x1="3" y1="11" x2="21" y2="11" />
    <line x1="12" y1="20" x2="12" y2="24" />
  </SvgWrapper>
);

/** Wind Turbine: 3 blades */
export const WindTurbineIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="12" y1="24" x2="12" y2="11" />
    <circle cx="12" cy="10" r="2" fill="currentColor" />
    <line x1="12" y1="10" x2="22" y2="5" />
    <line x1="12" y1="10" x2="6" y2="3" />
    <line x1="12" y1="10" x2="16" y2="19" />
  </SvgWrapper>
);

/** PV Array: stacked panels */
export const PVArrayIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <rect x="4" y="4" width="7" height="7" fill="none" />
    <line x1="5.5" y1="4" x2="5.5" y2="11" />
    <line x1="9.5" y1="4" x2="9.5" y2="11" />
    <line x1="4" y1="7.5" x2="11" y2="7.5" />
    <rect x="13" y="4" width="7" height="7" fill="none" />
    <line x1="14.5" y1="4" x2="14.5" y2="11" />
    <line x1="18.5" y1="4" x2="18.5" y2="11" />
    <line x1="13" y1="7.5" x2="20" y2="7.5" />
    <rect x="4" y="13" width="7" height="7" fill="none" />
    <line x1="5.5" y1="13" x2="5.5" y2="20" />
    <line x1="9.5" y1="13" x2="9.5" y2="20" />
    <line x1="4" y1="16.5" x2="11" y2="16.5" />
    <rect x="13" y="13" width="7" height="7" fill="none" />
    <line x1="14.5" y1="13" x2="14.5" y2="20" />
    <line x1="18.5" y1="13" x2="18.5" y2="20" />
    <line x1="13" y1="16.5" x2="20" y2="16.5" />
  </SvgWrapper>
);

// ===================== LOADS =====================

/** PQ Load: downward arrow style */
export const LoadIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="4" y1="13" x2="20" y2="13" />
    <line x1="12" y1="6" x2="12" y2="20" />
    <line x1="6" y1="13" x2="18" y2="13" strokeWidth="3" />
  </SvgWrapper>
);

/** Motor: circle with M inside */
export const MotorIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="10" fill="none" />
    <text x="12" y="16" textAnchor="middle" fontSize="14" fontWeight="bold" fill="currentColor" stroke="none">
      M
    </text>
  </SvgWrapper>
);

// ===================== TRANSMISSION =====================

/** Line: horizontal line */
export const LineIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="12" x2="22" y2="12" />
    <text x="12" y="10" textAnchor="middle" fontSize="6" fill="currentColor" stroke="none">
      R+jX
    </text>
  </SvgWrapper>
);

/** 2-Winding Transformer: two overlapping ellipses */
export const TransformerIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="12" y1="2" x2="12" y2="4" />
    <ellipse cx="8" cy="12" rx="6" ry="8" fill="none" />
    <ellipse cx="16" cy="12" rx="6" ry="8" fill="none" />
    <line x1="12" y1="20" x2="12" y2="22" />
  </SvgWrapper>
);

/** 3-Winding Transformer: three overlapping ellipses */
export const Transformer3WIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <ellipse cx="7" cy="12" rx="5" ry="7" fill="none" />
    <ellipse cx="12" cy="12" rx="5" ry="7" fill="none" />
    <ellipse cx="17" cy="12" rx="5" ry="7" fill="none" />
    <line x1="2" y1="12" x2="4" y2="12" />
    <line x1="20" y1="12" x2="22" y2="12" />
    <line x1="12" y1="19" x2="12" y2="22" />
  </SvgWrapper>
);

// ===================== PROTECTION =====================

/** Circuit Breaker */
export const BreakerIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="12" x2="7" y2="12" />
    <rect x="7" y="8" width="10" height="8" fill="none" />
    <line x1="17" y1="12" x2="22" y2="12" />
  </SvgWrapper>
);

/** Switch */
export const SwitchIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="12" x2="8" y2="12" />
    <circle cx="12" cy="12" r="5" fill="none" />
    <line x1="16" y1="12" x2="22" y2="12" />
  </SvgWrapper>
);

/** Isolator/Disconnect */
export const DisconnectIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="12" x2="8" y2="12" />
    <line x1="8" y1="12" x2="16" y2="6" />
    <line x1="16" y1="12" x2="22" y2="12" />
  </SvgWrapper>
);

/** Fuse */
export const FuseIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="12" x2="8" y2="12" />
    <rect x="8" y="9" width="8" height="6" fill="none" />
    <line x1="16" y1="12" x2="22" y2="12" />
  </SvgWrapper>
);

/** Recloser: circle with R */
export const RecloserIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="12" x2="6" y2="12" />
    <circle cx="12" cy="12" r="6" fill="none" />
    <text x="12" y="15" textAnchor="middle" fontSize="9" fontWeight="bold" fill="currentColor" stroke="none">
      R
    </text>
    <line x1="18" y1="12" x2="22" y2="12" />
  </SvgWrapper>
);

/** Relay: square with circle */
export const RelayIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="12" x2="6" y2="12" />
    <rect x="6" y="6" width="12" height="12" fill="none" />
    <circle cx="12" cy="12" r="4" fill="none" />
    <line x1="18" y1="12" x2="22" y2="12" />
  </SvgWrapper>
);

/** CT: circle with line through */
export const CTIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="12" y1="2" x2="12" y2="6" />
    <circle cx="12" cy="10" r="4" fill="none" />
    <line x1="8" y1="10" x2="16" y2="10" />
    <line x1="12" y1="14" x2="12" y2="22" />
  </SvgWrapper>
);

// ===================== COMPENSATION =====================

/** Capacitor: two parallel lines */
export const CapacitorIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="2" y1="12" x2="8" y2="12" />
    <line x1="8" y1="5" x2="8" y2="19" />
    <line x1="13" y1="5" x2="13" y2="19" />
    <line x1="13" y1="12" x2="22" y2="12" />
  </SvgWrapper>
);

/** Capacitor Bank */
export const CapacitorBankIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="12" y1="2" x2="12" y2="6" />
    <line x1="5" y1="10" x2="19" y2="10" />
    <line x1="5" y1="14" x2="19" y2="14" />
    <line x1="12" y1="14" x2="12" y2="22" />
  </SvgWrapper>
);

/** Shunt Reactor */
export const ShuntIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="12" y1="2" x2="12" y2="8" />
    <line x1="6" y1="13" x2="18" y2="13" />
    <line x1="6" y1="17" x2="18" y2="17" />
    <line x1="12" y1="17" x2="12" y2="22" />
  </SvgWrapper>
);

/** SVC: box with circle */
export const SvcIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="12" y1="2" x2="12" y2="6" />
    <rect x="4" y="6" width="16" height="12" fill="none" />
    <circle cx="12" cy="12" r="4" fill="none" />
    <text x="12" y="14" textAnchor="middle" fontSize="5" fill="currentColor" stroke="none">
      SVC
    </text>
    <line x1="12" y1="18" x2="12" y2="22" />
  </SvgWrapper>
);

/** Battery: multiple cells */
export const BatteryIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="6" y1="10" x2="6" y2="14" strokeWidth="2" />
    <line x1="10" y1="8" x2="10" y2="16" strokeWidth="2.5" />
    <line x1="14" y1="8" x2="14" y2="16" strokeWidth="2.5" />
    <line x1="18" y1="10" x2="18" y2="14" strokeWidth="2" />
  </SvgWrapper>
);

// ===================== NETWORK =====================

/** Ground */
export const GroundIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <line x1="12" y1="2" x2="12" y2="8" />
    <line x1="4" y1="8" x2="20" y2="8" strokeWidth="2.5" />
    <line x1="7" y1="13" x2="17" y2="13" strokeWidth="2" />
    <line x1="9" y1="18" x2="15" y2="18" strokeWidth="1.5" />
  </SvgWrapper>
);

/** Substation */
export const SubstationIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <rect x="3" y="3" width="18" height="18" fill="none" strokeDasharray="2 2" />
    <rect x="6" y="6" width="12" height="12" fill="none" />
    <text x="12" y="14" textAnchor="middle" fontSize="7" fontWeight="bold" fill="currentColor" stroke="none">
      SS
    </text>
  </SvgWrapper>
);

/** Meter: circle with V */
export const MeterIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="9" fill="none" />
    <text x="12" y="16" textAnchor="middle" fontSize="12" fontWeight="bold" fill="currentColor" stroke="none">
      V
    </text>
  </SvgWrapper>
);

/** Junction: filled circle */
export const JunctionIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="4" fill="currentColor" stroke="none" />
  </SvgWrapper>
);

// ===================== CONTROL =====================

/** AVR */
export const AvrIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <rect x="4" y="5" width="16" height="14" fill="none" />
    <text x="12" y="15" textAnchor="middle" fontSize="9" fontWeight="bold" fill="currentColor" stroke="none">
      AVR
    </text>
  </SvgWrapper>
);

/** Governor/TG */
export const GovernorIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <rect x="4" y="5" width="16" height="14" fill="none" />
    <text x="12" y="15" textAnchor="middle" fontSize="9" fontWeight="bold" fill="currentColor" stroke="none">
      TG
    </text>
  </SvgWrapper>
);

/** PSS */
export const PssIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <rect x="4" y="5" width="16" height="14" fill="none" />
    <text x="12" y="15" textAnchor="middle" fontSize="9" fontWeight="bold" fill="currentColor" stroke="none">
      PSS
    </text>
  </SvgWrapper>
);

/** LTC/Tap Changer */
export const LtciIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <rect x="4" y="5" width="16" height="14" fill="none" />
    <text x="12" y="15" textAnchor="middle" fontSize="9" fontWeight="bold" fill="currentColor" stroke="none">
      TAP
    </text>
  </SvgWrapper>
);

/** Area: dotted bounding box */
export const AreaIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <rect x="3" y="3" width="18" height="18" fill="none" strokeDasharray="3 2" />
    <text x="12" y="15" textAnchor="middle" fontSize="8" fontWeight="bold" fill="currentColor" stroke="none">
      AREA
    </text>
  </SvgWrapper>
);

/** FACTS: dashed circle with cross */
export const FactsIcon: React.FC<IconProps> = ({ size = 24, className = '' }) => (
  <SvgWrapper size={size} className={className} viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="9" fill="none" strokeDasharray="3 2" />
    <line x1="12" y1="3" x2="12" y2="21" />
    <line x1="3" y1="12" x2="21" y2="12" />
  </SvgWrapper>
);

// Map from symbol type to icon component
export const symbolIconMap: Record<string, React.FC<IconProps>> = {
  slack: SlackBusIcon,
  pv: PVBusIcon,
  pq: PQBusIcon,
  bus: PQBusIcon,
  generator: GeneratorIcon,
  load: LoadIcon,
  motor: MotorIcon,
  shunt: ShuntIcon,
  capacitor: CapacitorIcon,
  'capacitor-bank': CapacitorBankIcon,
  line: LineIcon,
  transformer: TransformerIcon,
  'transformer-3w': Transformer3WIcon,
  'transformer-reg': TransformerIcon,
  breaker: BreakerIcon,
  switch: SwitchIcon,
  disconnect: DisconnectIcon,
  fuse: FuseIcon,
  sectionalizer: SwitchIcon,
  recloser: RecloserIcon,
  'current-transformer': CTIcon,
  'potential-transformer': CTIcon,
  relay: RelayIcon,
  meter: MeterIcon,
  ground: GroundIcon,
  'external-grid': ExternalGridIcon,
  equivalent: GeneratorIcon,
  svc: SvcIcon,
  statcom: SvcIcon,
  tcsc: CapacitorIcon,
  upfc: SvcIcon,
  'wind-turbine': WindTurbineIcon,
  'pv-array': PVArrayIcon,
  battery: BatteryIcon,
  substation: SubstationIcon,
  junction: JunctionIcon,
  arrestor: GroundIcon,
  reactor: ShuntIcon,
};