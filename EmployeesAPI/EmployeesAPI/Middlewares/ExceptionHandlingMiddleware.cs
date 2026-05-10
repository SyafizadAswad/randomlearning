using System.Net;
using System.Text.Json;
using EmployeesAPI.Exceptions;

namespace EmployeesAPI.Middlewares
{
    public class ExceptionHandlingMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<ExceptionHandlingMiddleware> _logger;

        public ExceptionHandlingMiddleware(RequestDelegate next, ILogger<ExceptionHandlingMiddleware> logger)
        {
            _next = next;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            try
            {
                await _next(context);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "An unhandled exception occured");
                await HandleExceptionAsync(context, ex);
            }
        }

        private static Task HandleExceptionAsync(HttpContext context, Exception exception)
        {
            var code = HttpStatusCode.InternalServerError; // default to 500
            var result = string.Empty;

            // map custom exception to HTTP status code
            switch (exception)
            {
                case NotFoundException:
                    code = HttpStatusCode.NotFound; //404
                    break;
                case ConflictException:
                    code = HttpStatusCode.Conflict; // 409
                    break;
                case BadRequestException:
                    code = HttpStatusCode.BadRequest; // 400
                    break;
            }

            context.Response.ContentType = "application/json";
            context.Response.StatusCode = (int)code;

            // create a consistent error object for angular app to read
            result = JsonSerializer.Serialize(new
            {
                error = exception.GetType().Name,
                message = exception.Message
            });

            return context.Response.WriteAsync(result);
        }
    }
}
