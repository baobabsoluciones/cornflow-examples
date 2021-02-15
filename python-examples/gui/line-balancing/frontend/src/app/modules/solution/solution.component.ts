import { Component, OnInit, ViewChild } from '@angular/core';
import { Solution } from './solution';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { ConnectionService } from '../connection/connection.service';
import { updateTableUI } from '../functions/table-functions';

@Component({
  selector: 'app-solution',
  templateUrl: './solution.component.html',
  styleUrls: ['./solution.component.css']
})
export class SolutionComponent implements OnInit {

  solution: Solution[];
  public displayedColumns: string[] = ['task_name', 'station_name'];
  dataSource: MatTableDataSource<Solution>;
  
  @ViewChild('paginatorTable', { static: true }) paginatorTable: MatPaginator;
  @ViewChild('sortTable', { static: true }) sortTable: MatSort;

  constructor(private connection: ConnectionService) {
    this.dataSource = updateTableUI(
      this.solution,
      this.dataSource,
      this.paginatorTable,
      this.sortTable
    );
   }

  ngOnInit() {
    this.connection.getSolution('http://127.0.0.1:8000/solution/').subscribe((data) => {
      if (data.status === 200) {
        this.solution = data.body;
        this.dataSource = updateTableUI(
          this.solution,
          this.dataSource,
          this.paginatorTable,
          this.sortTable
        );
      }
    });
  }

}
