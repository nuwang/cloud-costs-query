import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'frontend';
  toolName: string = '';

  constructor(private http: HttpClient) { }

  onSubmit() {
    this.http.get<any>(`/runtime_90th_percentile/?tool_name=${this.toolName}`).subscribe(data => {
      const canvas = document.getElementById('myChart') as HTMLCanvasElement;
      const ctx = canvas.getContext('2d');

      if (ctx) { // Ensure ctx is not null
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['90th Percentile Runtime (s)'],
            datasets: [{
              label: this.toolName,
              data: [data['90th_percentile_runtime_seconds']],
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      } else {
        console.error('Failed to get 2D context');
      }
    }, error => {
      console.error('Error:', error);
    });   
  }  
}
