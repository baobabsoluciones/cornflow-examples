import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PrecedencesComponent } from './precedences.component';

describe('PrecedencesComponent', () => {
  let component: PrecedencesComponent;
  let fixture: ComponentFixture<PrecedencesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PrecedencesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PrecedencesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
