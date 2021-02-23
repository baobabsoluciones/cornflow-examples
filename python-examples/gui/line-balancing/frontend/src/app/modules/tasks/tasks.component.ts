import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { ConnectionService } from '../connection/connection.service';
import { updateTableUI } from '../functions/table-functions';
import { Tasks } from './tasks';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.css'],
})
export class TasksComponent implements OnInit {
  tasks: Tasks[];
  public displayedColumns: string[] = ['name', 'duration', 'actions'];
  dataSource: MatTableDataSource<Tasks>;

  @ViewChild('paginatorTable', { static: true }) paginatorTable: MatPaginator;
  @ViewChild('sortTable', { static: true }) sortTable: MatSort;

  constructor(private connection: ConnectionService) {
    this.dataSource = updateTableUI(
      this.tasks,
      this.dataSource,
      this.paginatorTable,
      this.sortTable
    );
  }

  ngOnInit() {
    this.connection.getTasks('http://127.0.0.1:8000/tasks/').subscribe(data => {
      if (data.status === 200) {
        this.tasks = data.body;
        this.dataSource = updateTableUI(
      this.tasks,
      this.dataSource,
      this.paginatorTable,
      this.sortTable
    );
      }
    });
}

new(): void {

}

edit(task: any): void {

}

delete(task: any): void {
  
}

}
