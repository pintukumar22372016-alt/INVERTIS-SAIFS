/* SAIFS Charts.js - Chart configurations */

const CHART_COLORS = {
  primary: '#6366f1',
  secondary: '#8b5cf6',
  success: '#10b981',
  warning: '#f59e0b',
  danger: '#ef4444',
  info: '#3b82f6',
  rose: '#f43f5e',
  teal: '#0d9488',
};

const isDark = () => document.documentElement.getAttribute('data-theme') !== 'light';

function chartDefaults(){
  return {
    color: isDark() ? '#94a3b8' : '#64748b',
    plugins:{
      legend:{labels:{color: isDark() ? '#94a3b8' : '#64748b', font:{family:'Inter',size:12}}},
      tooltip:{backgroundColor: isDark() ? 'rgba(30,41,59,0.95)' : 'rgba(255,255,255,0.95)',
        titleColor: isDark() ? '#f1f5f9' : '#0f172a',
        bodyColor: isDark() ? '#94a3b8' : '#64748b',
        borderColor: 'rgba(99,102,241,0.3)', borderWidth:1,
        padding:12, cornerRadius:10}
    },
    scales:{
      x:{grid:{color: isDark() ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)'},
         ticks:{color: isDark() ? '#94a3b8' : '#64748b', font:{family:'Inter'}}},
      y:{grid:{color: isDark() ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)'},
         ticks:{color: isDark() ? '#94a3b8' : '#64748b', font:{family:'Inter'}}}
    }
  };
}

/* Render Rating Doughnut */
window.renderRatingChart = function(canvasId, data){
  const ctx = document.getElementById(canvasId);
  if(!ctx) return;
  new Chart(ctx, {
    type:'doughnut',
    data:{
      labels:['1 ★','2 ★','3 ★','4 ★','5 ★'],
      datasets:[{
        data:[data['1']||0, data['2']||0, data['3']||0, data['4']||0, data['5']||0],
        backgroundColor:['#ef4444','#f97316','#f59e0b','#84cc16','#10b981'],
        borderWidth:0, hoverOffset:8
      }]
    },
    options:{
      responsive:true, maintainAspectRatio:false, cutout:'70%',
      plugins:{legend:{position:'bottom', ...chartDefaults().plugins.legend},
               tooltip:{...chartDefaults().plugins.tooltip}}
    }
  });
};

/* Render Complaint Status Pie */
window.renderComplaintChart = function(canvasId, data){
  const ctx = document.getElementById(canvasId);
  if(!ctx) return;
  new Chart(ctx, {
    type:'pie',
    data:{
      labels: Object.keys(data),
      datasets:[{
        data: Object.values(data),
        backgroundColor:[CHART_COLORS.warning, CHART_COLORS.info, CHART_COLORS.success, '#94a3b8'],
        borderWidth:0, hoverOffset:6
      }]
    },
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{position:'bottom', ...chartDefaults().plugins.legend},
               tooltip:{...chartDefaults().plugins.tooltip}}
    }
  });
};

/* Render Monthly Trend Line */
window.renderTrendChart = function(canvasId, labels, data){
  const ctx = document.getElementById(canvasId);
  if(!ctx) return;
  new Chart(ctx, {
    type:'line',
    data:{
      labels: labels,
      datasets:[{
        label:'Feedback',
        data: data,
        borderColor: CHART_COLORS.primary,
        backgroundColor:'rgba(99,102,241,0.12)',
        fill:true, tension:0.4, pointRadius:4,
        pointBackgroundColor: CHART_COLORS.primary,
        borderWidth:2
      }]
    },
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:false}, tooltip:{...chartDefaults().plugins.tooltip}},
      scales: chartDefaults().scales
    }
  });
};

/* Render Attendance Bar */
window.renderAttendanceChart = function(canvasId, present, absent, late){
  const ctx = document.getElementById(canvasId);
  if(!ctx) return;
  new Chart(ctx, {
    type:'bar',
    data:{
      labels:['Present','Absent','Late'],
      datasets:[{
        data:[present, absent, late],
        backgroundColor:[CHART_COLORS.success, CHART_COLORS.danger, CHART_COLORS.warning],
        borderRadius:8, borderWidth:0
      }]
    },
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:false}, tooltip:{...chartDefaults().plugins.tooltip}},
      scales:{
        x:{...chartDefaults().scales.x},
        y:{...chartDefaults().scales.y, beginAtZero:true}
      }
    }
  });
};

/* Render User Distribution Bar */
window.renderUserChart = function(canvasId, students, teachers, parents){
  const ctx = document.getElementById(canvasId);
  if(!ctx) return;
  new Chart(ctx, {
    type:'bar',
    data:{
      labels:['Students','Teachers','Parents'],
      datasets:[{
        data:[students, teachers, parents],
        backgroundColor:[CHART_COLORS.primary, CHART_COLORS.secondary, CHART_COLORS.teal],
        borderRadius:8, borderWidth:0
      }]
    },
    options:{
      responsive:true, maintainAspectRatio:false, indexAxis:'y',
      plugins:{legend:{display:false}, tooltip:{...chartDefaults().plugins.tooltip}},
      scales:{
        x:{...chartDefaults().scales.x, beginAtZero:true},
        y:{...chartDefaults().scales.y}
      }
    }
  });
};
