export class Precedence {
  id: number;
  before: number;
  after: number;
  before_name: string;
  after_name: string;

  constructor(
    id: number,
    before: number,
    after: number,
    before_name: string,
    after_name: string
  ) {
    this.id = id;
    this.before = before;
    this.after = after;
    this.before_name = before_name;
    this.after_name = after_name;
  }
}
