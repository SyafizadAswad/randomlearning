using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using EmployeesDataAccess.Models;
using EmployeesDataAccess.Interfaces;

namespace EmployeesDataAccess.Repositories
{
    public class DepartmentRepository : IDepartmentRepository
    {
        private readonly DataAccessContext _context;
        public DepartmentRepository(DataAccessContext context)
        {
            _context = context;
        }

        // GET
        public async Task<IEnumerable<Department>> GetAllDepartmentAsync()
        {
            return await _context.Department.ToListAsync();
        }
    }
}
