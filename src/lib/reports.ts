/**
 * Report Generation Module
 * Export power system analysis results to various formats
 */

import { PowerSystem, PowerFlowResult } from '@/types';
import { OPFResult } from './opf';
import { FaultStudyResult } from './fault';
import { TimeSeriesResult } from './timeseries';
import { StabilityAnalysisResult } from './stability';

// Report data structures
export interface ReportData {
  title: string;
  date: Date;
  system: PowerSystem;
  powerFlow?: PowerFlowResult;
  opf?: OPFResult;
  faultStudy?: FaultStudyResult;
  timeSeries?: TimeSeriesResult;
  stability?: StabilityAnalysisResult;
  notes?: string;
}

export interface ReportSection {
  title: string;
  content: string | string[][];
  type: 'text' | 'table' | 'chart' | 'image';
}

export interface ExportedReport {
  data: ReportData;
  sections: ReportSection[];
  format: 'html' | 'pdf' | 'csv' | 'json';
}

/**
 * Format number with units
 */
function formatNumber(num: number, decimals = 2): string {
  return num.toFixed(decimals);
}

/**
 * Format power in MW
 */
function formatPower(mw: number): string {
  if (Math.abs(mw) >= 1000) {
    return `${formatNumber(mw / 1000, 2)} GW`;
  }
  return `${formatNumber(mw, 2)} MW`;
}

/**
 * Format voltage in kV
 */
function formatVoltage(v: number, baseKV = 115): string {
  return `${formatNumber(v * baseKV, 2)} kV`;
}

/**
 * Generate system summary section
 */
function generateSystemSummary(system: PowerSystem): ReportSection {
  const buses = system.buses.filter(b => b.active).length;
  const generators = system.generators.filter(g => g.active).length;
  const loads = system.loads.filter(l => l.active).length;
  const lines = system.lines.filter(l => l.active).length;
  const transformers = (system.transformers || []).filter(t => t.active).length;
  
  const totalGen = system.generators.reduce((sum, g) => sum + (g.pg * (system.baseMVA || 100)), 0);
  const totalLoad = system.loads.reduce((sum, l) => sum + (l.pl * (system.baseMVA || 100)), 0);
  
  const content = [
    ['Category', 'Count'],
    ['Total Buses', buses.toString()],
    ['Generators', generators.toString()],
    ['Loads', loads.toString()],
    ['Transmission Lines', lines.toString()],
    ['Transformers', transformers.toString()],
    ['Total Generation', formatPower(totalGen)],
    ['Total Load', formatPower(totalLoad)],
    ['Base MVA', `${system.baseMVA || 100} MVA`],
    ['System Frequency', `${system.baseFreq || 60} Hz`]
  ];
  
  return {
    title: 'System Summary',
    content,
    type: 'table'
  };
}

/**
 * Generate power flow results section
 */
function generatePowerFlowSection(result: PowerFlowResult, system: PowerSystem): ReportSection[] {
  const sections: ReportSection[] = [];
  
  // Summary
  sections.push({
    title: 'Power Flow Results',
    content: [
      ['Parameter', 'Value'],
      ['Method', result.method || 'Newton-Raphson'],
      ['Converged', result.converged ? 'Yes' : 'No'],
      ['Iterations', result.iterations.toString()],
      ['Max Mismatch', formatNumber(result.maxMismatch || 0, 6)],
      ['Elapsed Time', `${result.elapsedTime?.toFixed(2) || 0} ms`]
    ],
    type: 'table'
  });
  
  // Bus results
  if (result.busResults && result.busResults.length > 0) {
    const busTable: string[][] = [
      ['Bus', 'Voltage (pu)', 'Angle (°)', 'P Gen (MW)', 'Q Gen (MVAR)', 'P Load (MW)', 'Q Load (MVAR)']
    ];
    
    result.busResults.forEach(bus => {
      const busData = system.buses.find(b => b.id === bus.bus);
      busTable.push([
        busData?.name || bus.bus,
        formatNumber(bus.v || 1.0, 4),
        formatNumber(bus.angle || 0, 2),
        formatNumber((bus.pg || 0) * (system.baseMVA || 100), 2),
        formatNumber((bus.qg || 0) * (system.baseMVA || 100), 2),
        formatNumber((bus.pl || 0) * (system.baseMVA || 100), 2),
        formatNumber((bus.ql || 0) * (system.baseMVA || 100), 2)
      ]);
    });
    
    sections.push({
      title: 'Bus Results',
      content: busTable,
      type: 'table'
    });
  }
  
  // Line results
  if (result.lineResults && result.lineResults.length > 0) {
    const lineTable: string[][] = [
      ['Line', 'From', 'To', 'P From (MW)', 'Q From (MVAR)', 'P To (MW)', 'Q To (MVAR)', 'Loading (%)']
    ];
    
    result.lineResults.forEach(line => {
      const lineData = system.lines.find(l => l.id === line.line);
      lineTable.push([
        lineData?.id || line.line,
        line.fromBus,
        line.toBus,
        formatNumber(line.pFrom || 0, 2),
        formatNumber(line.qFrom || 0, 2),
        formatNumber(line.pTo || 0, 2),
        formatNumber(line.qTo || 0, 2),
        formatNumber(line.loading || 0, 1)
      ]);
    });
    
    sections.push({
      title: 'Line Results',
      content: lineTable,
      type: 'table'
    });
  }
  
  return sections;
}

/**
 * Generate OPF results section
 */
function generateOPFSection(result: OPFResult): ReportSection[] {
  const sections: ReportSection[] = [];
  
  sections.push({
    title: 'Optimal Power Flow Results',
    content: [
      ['Parameter', 'Value'],
      ['Status', result.success ? 'Optimal' : 'Infeasible'],
      ['Total Cost', `$${formatNumber(result.totalCost || 0, 2)}/h`],
      ['Elapsed Time', `${result.elapsedTime?.toFixed(2) || 0} ms`],
      ['Generators', result.generatorResults?.length.toString() || '0']
    ],
    type: 'table'
  });
  
  if (result.generatorResults && result.generatorResults.length > 0) {
    const genTable: string[][] = [
      ['Generator', 'Bus', 'P (MW)', 'Q (MVAR)', 'V (pu)']
    ];
    
    result.generatorResults.forEach(gen => {
      genTable.push([
        gen.generator,
        gen.bus,
        formatNumber(gen.pg * 100, 2),
        formatNumber(gen.qg * 100, 2),
        formatNumber(gen.v || 1.0, 4)
      ]);
    });
    
    sections.push({
      title: 'Generator Dispatch',
      content: genTable,
      type: 'table'
    });
  }
  
  return sections;
}

/**
 * Generate fault study section
 */
function generateFaultSection(result: FaultStudyResult): ReportSection[] {
  const sections: ReportSection[] = [];
  
  sections.push({
    title: 'Fault Study Results',
    content: [
      ['Fault Type', 'Count'],
      ['Three-Phase', result.threePhaseFaults.length.toString()],
      ['Line-to-Ground', result.lineToGroundFaults.length.toString()],
      ['Line-to-Line', result.lineToLineFaults.length.toString()],
      ['Double Line-to-Ground', result.doubleLineToGroundFaults.length.toString()]
    ],
    type: 'table'
  });
  
  if (result.threePhaseFaults.length > 0) {
    const faultTable: string[][] = [
      ['Bus', 'Fault MVA', 'CT Rating (A)']
    ];
    
    result.threePhaseFaults.forEach(fault => {
      faultTable.push([
        fault.bus,
        formatNumber(fault.faultMVA, 2),
        formatNumber(fault.ctRating, 1)
      ]);
    });
    
    sections.push({
      title: 'Three-Phase Fault Currents',
      content: faultTable,
      type: 'table'
    });
  }
  
  if (result.protectiveDeviceRequirements.length > 0) {
    const devTable: string[][] = [
      ['Bus', 'Min Breaker (MVA)', 'Rec. Breaker (MVA)', 'Pickup (A)', 'Time Delay (s)']
    ];
    
    result.protectiveDeviceRequirements.forEach(dev => {
      devTable.push([
        dev.bus,
        formatNumber(dev.minBreakerRating, 2),
        formatNumber(dev.recommendedBreakerRating, 2),
        formatNumber(dev.relaySettings.pickup, 1),
        formatNumber(dev.relaySettings.timeDelay, 2)
      ]);
    });
    
    sections.push({
      title: 'Protective Device Requirements',
      content: devTable,
      type: 'table'
    });
  }
  
  return sections;
}

/**
 * Generate stability section
 */
function generateStabilitySection(result: StabilityAnalysisResult): ReportSection[] {
  const sections: ReportSection[] = [];
  
  sections.push({
    title: 'Small Signal Stability Analysis',
    content: [
      ['Parameter', 'Value'],
      ['Total Modes', result.eigenvalues.length.toString()],
      ['Unstable Modes', result.unstableModes.length.toString()],
      ['Poorly Damped', result.criticallyDampedModes.length.toString()],
      ['System Damping', result.systemDamping || 'unknown']
    ],
    type: 'table'
  });
  
  if (result.leastDampedMode) {
    sections.push({
      title: 'Least Damped Mode',
      content: [
        ['Parameter', 'Value'],
        ['Frequency', `${formatNumber(result.leastDampedMode.frequency, 3)} Hz`],
        ['Damping Ratio', formatNumber(result.leastDampedMode.dampingRatio, 4)],
        ['Mode Type', result.leastDampedMode.modeType],
        ['Status', result.leastDampedMode.damping]
      ],
      type: 'table'
    });
  }
  
  return sections;
}

/**
 * Generate complete report
 */
export function generateReport(data: ReportData): ReportSection[] {
  const sections: ReportSection[] = [
    {
      title: 'Report Information',
      content: [
        ['Title', data.title],
        ['Date', data.date.toISOString()],
        ['System Name', data.system.areas?.[0]?.name || 'Power System']
      ],
      type: 'table'
    },
    generateSystemSummary(data.system)
  ];
  
  if (data.powerFlow) {
    sections.push(...generatePowerFlowSection(data.powerFlow, data.system));
  }
  
  if (data.opf) {
    sections.push(...generateOPFSection(data.opf));
  }
  
  if (data.faultStudy) {
    sections.push(...generateFaultSection(data.faultStudy));
  }
  
  if (data.stability) {
    sections.push(...generateStabilitySection(data.stability));
  }
  
  if (data.notes) {
    sections.push({
      title: 'Notes',
      content: data.notes,
      type: 'text'
    });
  }
  
  return sections;
}

/**
 * Export report as HTML
 */
export function exportReportAsHTML(report: ReportSection[], title: string): string {
  let html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>${title}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; color: #333; }
    h1 { color: #1a5276; border-bottom: 2px solid #1a5276; padding-bottom: 10px; }
    h2 { color: #2874a6; margin-top: 30px; }
    table { border-collapse: collapse; width: 100%; margin: 15px 0; }
    th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
    th { background-color: #2874a6; color: white; }
    tr:nth-child(even) { background-color: #f9f9f9; }
    .footer { margin-top: 40px; font-size: 12px; color: #666; border-top: 1px solid #ddd; padding-top: 20px; }
  </style>
</head>
<body>
  <h1>${title}</h1>
`;
  
  report.forEach(section => {
    html += `<h2>${section.title}</h2>`;
    
    if (section.type === 'table' && Array.isArray(section.content)) {
      html += '<table><thead><tr>';
      const rows = section.content as string[][];
      rows[0].forEach(cell => {
        html += `<th>${cell}</th>`;
      });
      html += '</tr></thead><tbody>';
      rows.slice(1).forEach(row => {
        html += '<tr>';
        row.forEach(cell => {
          html += `<td>${cell}</td>`;
        });
        html += '</tr>';
      });
      html += '</tbody></table>';
    } else if (section.type === 'text') {
      html += `<p>${section.content}</p>`;
    }
  });
  
  html += `
  <div class="footer">
    Generated by PSAT Web - Power System Analysis Tool<br>
    ${new Date().toLocaleString()}
  </div>
</body>
</html>`;
  
  return html;
}

/**
 * Export report as CSV
 */
export function exportReportAsCSV(report: ReportSection[]): string {
  let csv = '';
  
  report.forEach(section => {
    csv += `\n# ${section.title}\n`;
    
    if (Array.isArray(section.content)) {
      const rows = section.content as string[][];
      rows.forEach(row => {
        csv += row.map(cell => `"${cell}"`).join(',') + '\n';
      });
    } else {
      csv += `"${section.content}"\n`;
    }
  });
  
  return csv;
}

/**
 * Export report as JSON
 */
export function exportReportAsJSON(report: ReportSection[]): string {
  return JSON.stringify(report, null, 2);
}

/**
 * Download report
 */
export function downloadReport(
  report: ReportSection[],
  title: string,
  format: 'html' | 'csv' | 'json'
): void {
  let content: string;
  let mimeType: string;
  let extension: string;
  
  switch (format) {
    case 'html':
      content = exportReportAsHTML(report, title);
      mimeType = 'text/html';
      extension = 'html';
      break;
    case 'csv':
      content = exportReportAsCSV(report);
      mimeType = 'text/csv';
      extension = 'csv';
      break;
    case 'json':
      content = exportReportAsJSON(report);
      mimeType = 'application/json';
      extension = 'json';
      break;
  }
  
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${title.replace(/\s+/g, '_')}.${extension}`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
