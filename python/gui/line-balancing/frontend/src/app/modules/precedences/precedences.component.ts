import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material';
import { Precedence } from './precedences';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { ConnectionService } from '../connection/connection.service';
import { updateTableUI } from '../functions/table-functions';

@Component({
  selector: 'app-precedences',
  templateUrl: './precedences.component.html',
  styleUrls: ['./precedences.component.css'],
})
export class PrecedencesComponent implements OnInit {
  precedences: Precedence[];
  public displayedColumns: string[] = ['before_name', 'after_name', 'actions'];
  dataSource: MatTableDataSource<Precedence>;

  @ViewChild('paginatorTable', { static: true }) paginatorTable: MatPaginator;
  @ViewChild('sortTable', { static: true }) sortTable: MatSort;

  constructor(private connection: ConnectionService) {
    this.dataSource = updateTableUI(
      this.precedences,
      this.dataSource,
      this.paginatorTable,
      this.sortTable
    );
  }

  ngOnInit() {
    this.connection.getPrecedences('http://127.0.0.1:8000/precedences/').subscribe(data => {
      if (data.status === 200) {
        this.precedences = data.body;
        this.dataSource = updateTableUI(
      this.precedences,
      this.dataSource,
      this.paginatorTable,
      this.sortTable
    );
      }
    });
  }

  new(): void {

  }

  edit(precedence: any): void {

  }

  delete(precedence: any): void {

  }
}
