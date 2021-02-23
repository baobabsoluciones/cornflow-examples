import { Component, OnInit, ViewChild } from '@angular/core';
import { Station } from './stations';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { ConnectionService } from '../connection/connection.service';
import { updateTableUI } from '../functions/table-functions';

@Component({
  selector: 'app-stations',
  templateUrl: './stations.component.html',
  styleUrls: ['./stations.component.css'],
})
export class StationsComponent implements OnInit {
  stations: Station[];
  public displayedColumns: string[] = ['name', 'no_position', 'order', 'actions'];
  dataSource: MatTableDataSource<Station>;
  
  @ViewChild('paginatorTable', { static: true }) paginatorTable: MatPaginator;
  @ViewChild('sortTable', { static: true }) sortTable: MatSort;

  constructor(
    private connection: ConnectionService
  ) {
    this.dataSource = updateTableUI(
      this.stations,
      this.dataSource,
      this.paginatorTable,
      this.sortTable
    );
  }

  ngOnInit() {
    this.connection.getStations('http://127.0.0.1:8000/stations/').subscribe((data) => {
      if (data.status === 200) {
        this.stations = data.body;
        this.dataSource = updateTableUI(
          this.stations,
          this.dataSource,
          this.paginatorTable,
          this.sortTable
        );
      }
    });
  }

  new(): void {

  }

  edit(station: any): void {

  }

  delete(station: any): void {
    
  }
}
