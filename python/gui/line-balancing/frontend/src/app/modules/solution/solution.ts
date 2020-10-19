export class Solution {
  id: number;
  station: number;
  task: number;
  station_name: string;
  task_name: string;

  constructor(
    id: number,
    station: number,
    task: number,
    station_name: string,
    task_name: string
  ) {
    this.id = id;
    this.station = station;
    this.task = task;
    this.station_name = station_name;
    this.task_name = task_name;
  }
}
