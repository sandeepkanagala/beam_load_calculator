// Beam Visualizer
const beamVisualizer = {
  initializeBeamDiagram() {
    const canvas = document.getElementById('beam-diagram');
    if (canvas) {
      const ctx = canvas.getContext('2d');
      canvas.width = 800;
      canvas.height = 200;
      this.drawBeamDiagram(ctx, canvas.width, canvas.height);
    }
  },

  drawBeamDiagram(ctx, width, height) {
    const beamParams = this.getBeamParameters();
    const loads = this.getLoads();

    ctx.clearRect(0, 0, width, height);

    const beamY = height / 2;
    const beamStartX = 50;
    const beamEndX = width - 50;
    const beamLength = beamEndX - beamStartX;
    const scale = beamLength / beamParams.length;

    // Draw beam
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(beamStartX, beamY);
    ctx.lineTo(beamEndX, beamY);
    ctx.stroke();

    // Draw supports
    this.drawSupport(ctx, beamStartX, beamY);
    this.drawSupport(ctx, beamEndX, beamY);

    // Draw point loads
    if (loads.pointLoads && loads.pointLoads.length > 0) {
      loads.pointLoads.forEach((load, index) => {
        const x = beamStartX + (load.position * scale);
        if (load.type === 'center') {
          this.drawPointLoadCenter(ctx, x, beamY - 50, load.magnitude, `P${index + 1}`);
        } else if (load.type === 'anywhere') {
          this.drawPointLoadAtPosition(ctx, x, beamY - 50, load.magnitude, `P${index + 1}`);
        }
      });
    }

    // Draw UDL
    if (loads.udl && loads.udl.magnitude > 0) {
      const startX = beamStartX + (loads.udl.start * scale);
      const endX = beamStartX + (loads.udl.end * scale);
      this.drawUDL(ctx, startX, endX, beamY - 40, loads.udl.magnitude);
    }

    // Draw UVL
    if (loads.uvl && loads.uvl.magnitude > 0) {
      const startX = beamStartX;
      const endX = beamStartX + (beamParams.length * scale);
      this.drawUVL(ctx, startX, endX, beamY - 45, loads.uvl.magnitude);
    }

    // Draw Moment
    if (loads.moment && loads.moment.magnitude !== 0) {
      const mX = beamStartX + (beamParams.length / 2) * scale;
      this.drawMoment(ctx, mX, beamY, loads.moment.magnitude);
    }

    // Dimensions and material
    ctx.fillStyle = '#666';
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`L = ${beamParams.length}m`, (beamStartX + beamEndX) / 2, beamY + 40);
    ctx.font = '12px Arial';
    ctx.fillText(`${beamParams.section.name} - ${beamParams.material.name}`, (beamStartX + beamEndX) / 2, beamY + 55);
  },

  drawSupport(ctx, x, y) {
    ctx.fillStyle = '#333';
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x - 12, y + 25);
    ctx.lineTo(x + 12, y + 25);
    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x - 15, y + 25);
    ctx.lineTo(x + 15, y + 25);
    ctx.stroke();
  },

  drawPointLoadCenter(ctx, x, y, magnitude, label = 'P') {
    ctx.strokeStyle = '#27ae60';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x, y + 40);
    ctx.stroke();

    ctx.fillStyle = '#27ae60';
    ctx.beginPath();
    ctx.moveTo(x, y + 40);
    ctx.lineTo(x - 6, y + 32);
    ctx.lineTo(x + 6, y + 32);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = '#27ae60';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`${label}: ${magnitude/1000}kN`, x, y - 10);
  },

  drawPointLoadAtPosition(ctx, x, y, magnitude, label = 'P') {
    ctx.strokeStyle = '#e74c3c';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x, y + 40);
    ctx.stroke();

    ctx.fillStyle = '#e74c3c';
    ctx.beginPath();
    ctx.moveTo(x, y + 40);
    ctx.lineTo(x - 6, y + 32);
    ctx.lineTo(x + 6, y + 32);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = '#e74c3c';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`${label}: ${magnitude}kN`, x, y - 10);
  },

  drawUDL(ctx, startX, endX, y, magnitude) {
    ctx.strokeStyle = '#3498db';
    ctx.lineWidth = 2;
    const numArrows = Math.max(5, Math.floor((endX - startX) / 25));
    for (let i = 0; i <= numArrows; i++) {
      const x = startX + (i * (endX - startX) / numArrows);
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x, y + 25);
      ctx.stroke();

      ctx.fillStyle = '#3498db';
      ctx.beginPath();
      ctx.moveTo(x, y + 25);
      ctx.lineTo(x - 4, y + 18);
      ctx.lineTo(x + 4, y + 18);
      ctx.closePath();
      ctx.fill();
    }

    ctx.beginPath();
    ctx.moveTo(startX, y);
    ctx.lineTo(endX, y);
    ctx.stroke();

    ctx.fillStyle = '#3498db';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`UDL: ${magnitude/1000}kN/m`, (startX + endX) / 2, y - 10);
  },

  drawUVL(ctx, startX, endX, y, maxMagnitude) {
  ctx.strokeStyle = '#8e44ad';
  ctx.fillStyle = '#8e44ad';
  ctx.lineWidth = 2;

  const steps = 10;
  const dx = (endX - startX) / steps;
  const maxArrowHeight = 30;

  for (let i = 0; i <= steps; i++) {
    const x = startX + i * dx;
    const factor = i / steps; 
    const arrowHeight = factor * maxArrowHeight;

    // Arrow line
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x, y + arrowHeight);
    ctx.stroke();

    // Arrowhead
    if (arrowHeight > 0) {
      ctx.beginPath();
      ctx.moveTo(x, y + arrowHeight);
      ctx.lineTo(x - 4, y + arrowHeight - 8);
      ctx.lineTo(x + 4, y + arrowHeight - 8);
      ctx.closePath();
      ctx.fill();
    }
  }
  ctx.font = '12px Arial';
  ctx.textAlign = 'center';
  ctx.fillText(`UVL: ${maxMagnitude/1000} kN/m`, (startX + endX) / 2, y - 10);
},



  drawMoment(ctx, x, y, magnitude) {
    ctx.beginPath();
    ctx.arc(x, y, 20, 0, Math.PI, magnitude > 0);
    ctx.strokeStyle = '#f39c12';
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.fillStyle = '#f39c12';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`M = ${magnitude/1000}kNm`, x, y - 30);
  },

  getBeamParameters() {
    const beam = window.beamData || {};
    const b = parseFloat(beam.b) || 300;
    const d = parseFloat(beam.d) || 500;
    const length = parseFloat(beam.length) || 5;
    return {
      length: length,
      section: { name: `${b}×${d} mm` },
      material: { name: beam.material || 'M20' }
    };
  },

  getLoads() {
    const beam = window.beamData || {};
    const type = beam.loadType || 'udl';
    const loadData = {
      pointLoads: [],
      udl: { magnitude: 0, start: 0, end: 0 },
      uvl: { magnitude: 0 },
      moment: { magnitude: 0 }
    };
    const L = parseFloat(beam.length) || 5;

    if (type === 'point_center') {
      const P = parseFloat(beam.P) || 0;
      loadData.pointLoads.push({ type: 'center', position: L / 2, magnitude: P });
    } else if (type === 'point_anywhere') {
      const P = parseFloat(beam.P) || 0;
      const a = parseFloat(beam.a) || 0;
      loadData.pointLoads.push({ type: 'anywhere', position: a, magnitude: P });
    } else if (type === 'udl') {
      loadData.udl = { magnitude: parseFloat(beam.w) || 0, start: 0, end: L };
    } else if (type === 'uvl') {
      loadData.uvl = { magnitude: parseFloat(beam.w_max) || 0 };
    } else if (type === 'moment') {
      loadData.moment = { magnitude: parseFloat(beam.M_applied) || 0 };
    }

    return loadData;
  }
};

window.addEventListener('DOMContentLoaded', () => {
  beamVisualizer.initializeBeamDiagram();
});
