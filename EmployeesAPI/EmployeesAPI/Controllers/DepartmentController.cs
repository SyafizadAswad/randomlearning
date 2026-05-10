using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using EmployeesDataAccess;
using EmployeesDataAccess.Models;

namespace EmployeesAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class DepartmentController : ControllerBase
    {
        private readonly DataAccessContext _context;

        public DepartmentController(DataAccessContext context)
        {
            _context = context;
        }

        // GET all department
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Department>>> GetDepartment()
        {
            return await _context.Department.ToListAsync();
        }

    }
}
