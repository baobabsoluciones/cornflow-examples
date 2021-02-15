import { HttpClient, HttpResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Station } from '../stations/stations';
import { Tasks } from '../tasks/tasks';
import { Precedence } from '../precedences/precedences';
import { Solution } from '../solution/solution';

const headers_object = new HttpHeaders();
headers_object.append('Content-Type', 'application/json');
headers_object.append('Authorization', 'Basic ' + btoa('None:None'));

@Injectable({
  providedIn: 'root'
})
export class ConnectionService {

  constructor(private http: HttpClient) { }

  getBase(url: string): Observable<HttpResponse<any[]>> {
    return this.http.get<any[]>(url, {
      headers: headers_object,
      observe: 'response',
    });
  }

  getStations(url: string): Observable<HttpResponse<Station[]>> {
    return this.getBase(url);
  }

  getTasks(url: string): Observable<HttpResponse<Tasks[]>> {
    return this.getBase(url);
  }

  getPrecedences(url: string): Observable<HttpResponse<Precedence[]>> {
    return this.getBase(url);
  }

  getSolution(url: string): Observable<HttpResponse<Solution[]>> {
    return this.getBase(url);
  }

  getSolve(url: string): Observable<HttpResponse<Solution[]>> {
    return this.getBase(url);
  }
}
