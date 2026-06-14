import { PowerSystem, PowerFlowResult, CPFResult, EigenvalueResult, SimulationResult, OPFResult } from '@/types';

export class ReportGenerator {
  static powerFlowReport(system: PowerSystem, result: PowerFlowResult): string {
    const lines: string[] = [];
    const hr = '='.repeat(72);
    const hr2 = '-'.repeat(72);

    lines.push(hr);
    lines.push('  PSAT POWER FLOW REPORT');
    lines.push(hr);
    lines.push(`  System: ${system.areas.map(a => a.name).join(', ') || 'Untitled'}`);
    lines.push(`  Date: ${new Date().toLocaleString()}`);
    lines.push(`  Buses: ${system.buses.length}  Lines: ${system.lines.length}  Generators: ${system.generators.length}  Loads: ${system.loads.length}`);
    lines.push(hr);

    lines.push('');
    lines.push('  SOLUTION SUMMARY');
    lines.push(hr2);
    lines.push(`  Converged:          ${result.converged ? 'YES' : 'NO'}`);
    lines.push(`  Iterations:         ${result.iterations}`);
    lines.push(`  Max Mismatch:       ${result.maxMismatch.toExponential(4)}`);
    lines.push(`  Slack Bus Angle:    ${result.slackAngle.toFixed(4)} deg`);
    lines.push(`  Total Losses (P):   ${result.losses.real.toFixed(6)} pu`);
    lines.push(`  Total Losses (Q):   ${result.losses.reactive.toFixed(6)} pu`);
    lines.push(hr2);

    lines.push('');
    lines.push('  BUS RESULTS');
    lines.push(hr2);
    lines.push('  Bus ID  Name           Type       V (pu)     Angle(deg)  Pg(pu)    Qg(pu)    Pd(pu)    Qd(pu)');
    lines.push(hr2);
    result.busResults.forEach(br => {
      const bus = system.buses.find(b => b.id === br.id);
      if (!bus) return;
      lines.push(`  ${br.id.padEnd(6)} ${bus.name.padEnd(13)} ${bus.type.toUpperCase().padEnd(9)} ${br.voltage.toFixed(5).padStart(9)} ${br.angle.toFixed(3).padStart(10)} ${br.pGen.toFixed(5).padStart(8)} ${br.qGen.toFixed(5).padStart(8)} ${br.pLoad.toFixed(5).padStart(8)} ${br.qLoad.toFixed(5).padStart(8)}`);
    });

    lines.push('');
    lines.push('  LINE RESULTS');
    lines.push(hr2);
    lines.push('  Line ID   From->To      P From(pu) Q From(pu) P To(pu)   Q To(pu)   Loading(%)');
    lines.push(hr2);
    result.lineResults.forEach(lr => {
      const line = system.lines.find(l => l.id === lr.id);
      if (!line) return;
      lines.push(`  ${lr.id.padEnd(9)} ${line.fromBus}->${line.toBus.padEnd(8)} ${lr.pFrom.toFixed(5).padStart(10)} ${lr.qFrom.toFixed(5).padStart(10)} ${lr.pTo.toFixed(5).padStart(9)} ${lr.qTo.toFixed(5).padStart(9)} ${lr.loading.toFixed(2).padStart(9)}`);
    });

    lines.push('');
    lines.push(hr);
    return lines.join('\n');
  }

  static eigenvalueReport(result: EigenvalueResult): string {
    const lines: string[] = [];
    lines.push('='.repeat(72));
    lines.push('  PSAT EIGENVALUE ANALYSIS REPORT');
    lines.push('='.repeat(72));
    lines.push(`  ${result.eigenvalues.length} eigenvalues computed`);
    lines.push('-'.repeat(72));
    lines.push('');
    lines.push('  Eigenvalue          Frequency(Hz)    Damping Ratio');
    lines.push('-'.repeat(72));

    result.eigenvalues.slice(0, 20).forEach((ev, i) => {
      const freq = result.frequencies[i] || 0;
      const damp = result.dampingRatios[i] || 0;
      const reStr = ev.real >= 0 ? ` ${ev.real.toFixed(6)}` : `${ev.real.toFixed(6)}`;
      const imStr = ev.imag >= 0 ? `+${ev.imag.toFixed(6)}i` : `${ev.imag.toFixed(6)}i`;
      const stable = ev.real < 0 ? ' (stable)' : ' (UNSTABLE)';
      lines.push(`  ${reStr} ${imStr.padEnd(15)} ${freq.toFixed(6).padStart(10)}    ${damp.toFixed(6).padStart(10)}${stable}`);
    });

    const unstable = result.eigenvalues.filter(ev => ev.real > 1e-6);
    if (unstable.length > 0) {
      lines.push('');
      lines.push(`  WARNING: ${unstable.length} unstable eigenvalue(s) detected!`);
    }

    lines.push('-'.repeat(72));
    return lines.join('\n');
  }

  static cpfReport(result: CPFResult): string {
    const lines: string[] = [];
    lines.push('='.repeat(72));
    lines.push('  PSAT CONTINUATION POWER FLOW REPORT');
    lines.push('='.repeat(72));
    lines.push(`  Converged:          ${result.converged ? 'YES' : 'NO'}`);
    lines.push(`  Points Computed:    ${result.points.length}`);
    lines.push(`  Critical Lambda:    ${result.criticalLambda.toFixed(6)}`);
    lines.push(`  Critical Bus:       ${result.criticalBus || 'N/A'}`);
    lines.push('-'.repeat(72));
    lines.push('');
    lines.push('  PV CURVE DATA (lambda, voltage at critical bus)');
    lines.push('-'.repeat(72));
    lines.push('  Step   Lambda      Voltage(pu)');
    lines.push('-'.repeat(72));
    result.noseCurve.forEach((pt, i) => {
      lines.push(`  ${(i + 1).toString().padStart(4)}  ${pt.lambda.toFixed(6).padStart(10)}  ${pt.voltage.toFixed(6).padStart(10)}`);
    });
    lines.push('-'.repeat(72));
    return lines.join('\n');
  }

  static simulationReport(result: SimulationResult): string {
    const n = result.time.length;
    const lines: string[] = [];
    lines.push('='.repeat(72));
    lines.push('  PSAT TIME DOMAIN SIMULATION REPORT');
    lines.push('='.repeat(72));
    lines.push(`  Time Points: ${n}`);
    lines.push(`  Duration: ${result.time[n - 1]?.toFixed(2) || 0}s to ${(result.time[0] || 0).toFixed(2)}s`);
    lines.push('-'.repeat(72));
    lines.push('');
    lines.push('  FINAL VALUES');
    lines.push('-'.repeat(72));

    const lastIdx = n - 1;
    Object.entries(result.busVoltages).forEach(([busId, values]) => {
      const v = values[lastIdx] || 0;
      const a = result.busAngles[busId]?.[lastIdx] || 0;
      lines.push(`  Bus ${busId}: V = ${v.toFixed(5)} pu, Angle = ${a.toFixed(3)} deg`);
    });

    lines.push('-'.repeat(72));
    return lines.join('\n');
  }

  static opfReport(result: OPFResult): string {
    const lines: string[] = [];
    lines.push('='.repeat(72));
    lines.push('  PSAT OPTIMAL POWER FLOW REPORT');
    lines.push('='.repeat(72));
    lines.push(`  Converged:          ${result.converged ? 'YES' : 'NO'}`);
    lines.push(`  Iterations:         ${result.iterations}`);
    lines.push(`  Objective Value:    ${result.objectiveValue.toFixed(6)}`);
    lines.push(`  Total Cost:         ${result.totalCost.toFixed(6)}`);
    lines.push('-'.repeat(72));
    lines.push('');
    lines.push('  SHADOW PRICES (Locational Marginal Prices)');
    lines.push('-'.repeat(72));
    Object.entries(result.shadowPrices).forEach(([busId, price]) => {
      lines.push(`  Bus ${busId}: ${price.toFixed(4)} $/MWh`);
    });
    lines.push('-'.repeat(72));
    return lines.join('\n');
  }
}
