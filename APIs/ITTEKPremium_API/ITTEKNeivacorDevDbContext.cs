using ITTEKPremium_API.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ITTEKPremium_API.Context
{
	public class ITTEKPrintNeivacorDevDbContext : DbContext
	{
		public ITTEKPrintNeivacorDevDbContext(DbContextOptions<ITTEKPrintNeivacorDevDbContext> options)
		: base(options)
		{
		}

		public DbSet<Stoves> Stoves { get; set; }
		
	}
}