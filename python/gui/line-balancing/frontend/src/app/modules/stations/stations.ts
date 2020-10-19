export class Station {
  id: number;
  name: string;
  no_position: number;
  order: number;

  constructor(id: number, name: string, no_position: number, order: number) {
    this.id = id;
    this.name = name;
    this.no_position = no_position;
    this.order = order;
  }
}
