export class Tasks {
  id: number;
  name: string;
  duration: number;

  constructor(id: number, name: string, duration: number) {
    this.id = id;
    this.name = name;
    this.duration = duration;
  }
}
