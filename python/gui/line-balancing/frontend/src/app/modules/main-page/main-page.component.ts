import { Component, OnInit } from '@angular/core';
import { ConnectionService } from '../connection/connection.service';
import { SpinnerComponent } from './spinner/spinner.component';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { Solution } from '../solution/solution';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.css'],
})
export class MainPageComponent implements OnInit {
  pad = 0;
  case_name = '';
  solution: Solution[];

  constructor(
    private dialog: MatDialog,
    private connection: ConnectionService
  ) {}

  ngOnInit() {}

  onActivate(componentReference) {
    if (componentReference.searchItem !== undefined) {
      componentReference.searchItem.subscribe((data) => {
        this.case_name = data;
      });
    }
  }

  public changepad() {
    this.pad = 1 - this.pad;
  }

  solve(): void {
    const dialogRef: MatDialogRef<SpinnerComponent> = this.dialog.open(
      SpinnerComponent,
      { panelClass: 'transparent', disableClose: true }
    );
    const subscription = this.connection.getSolve('http://127.0.0.1:8000/solve/').subscribe((data) => {
      if (data.status === 200) {
        this.solution = data.body;
      }
      subscription.unsubscribe();
      dialogRef.close();
    });
  }
}
