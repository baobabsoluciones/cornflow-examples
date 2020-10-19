import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

export function updateTableUI(
  array: any[],
  datasource: MatTableDataSource<any>,
  paginator: MatPaginator,
  sorter: MatSort
): MatTableDataSource<any> {
  datasource = new MatTableDataSource(array);
  datasource.paginator = paginator;
  datasource.sort = sorter;
  return datasource;
}
