import { HttpInterceptorFn, HttpRequest, HttpHandlerFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { ToastService } from '../services/toast.service';


export const AuthInterceptor: HttpInterceptorFn = (req: HttpRequest<any>, next: HttpHandlerFn) => {
    const authService = inject(AuthService);
    const router = inject(Router) as Router;
    const token = authService.getToken();
    const toast = inject(ToastService);

    if (token) {
        req = req.clone({
            setHeaders: {
                Authorization: `Bearer ${token}`
            }
        });
    }

    return next(req).pipe(
        catchError((err: HttpErrorResponse) => {
            // 1. handle 401 exclusively
            if (err.status === 401) {
                toast.show('Session expired. Please log in again.', 'error');
                authService.logout();
                try {
                    router.navigate(['/login']);
                } catch {
                    // ignore navigation errors
                }
                return throwError(() => err);
            }

            // 2. every other error
            const msg = err.error?.message || 'Something went wrong. Try again.';
            toast.show(msg, 'error');
            return throwError(() => err);
        })
    );
};
