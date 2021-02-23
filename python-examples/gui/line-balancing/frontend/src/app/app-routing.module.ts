import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MainPageComponent } from './modules/main-page/main-page.component';
import { PrecedencesComponent } from './modules/precedences/precedences.component';
import { StationsComponent } from './modules/stations/stations.component';
import { TasksComponent } from './modules/tasks/tasks.component';
import { SolutionComponent } from './modules/solution/solution.component';

const routes: Routes = [
  {
    path: 'main',
    component: MainPageComponent,
    children: [
      { path: '', redirectTo: 'stations', pathMatch: 'full' },
      { path: 'stations', component: StationsComponent },
      { path: 'tasks', component: TasksComponent },
      { path: 'precedences', component: PrecedencesComponent },
      { path: 'solution', component: SolutionComponent },
    ],
  },
  { path: '', redirectTo: 'main', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
