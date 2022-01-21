
Vue.component('vue-multiselect', window.VueMultiselect.default)
Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)

var app = new Vue({
   el: '#app',
   data: {
      isLoading: true,
      jobs: [],
      error: '',
      companies: [],
      selectedCompanies: [],
      recentJobs: [],
      textFilter: '',
      currentPage: 1,
      totalOfPages: 0,
      itemsPerPage: 10,
      currentView: 0,
      views: [
         'New jobs',
         'Search',
         'Tags analysis'
      ]
   },
   mounted: function () {
      this.loadJobs();
   },
   computed: {
      filteredJobs: function () {
         
         if (this.isLoading) {
            return [];
         }

         if (this.currentView == 0) {
            return this.recentJobs;
         }
         
         const companyNames = this.selectedCompanies.map(company => company.name);

         return this.jobs.filter(job => {
            return companyNames.includes(job.company) && (this.textFilter.length < 2 || job.filters.includes(this.textFilter.toLowerCase()));
         });
      },
      paggedJobs: function () {
         
         if (this.currentView == 0) {
            return this.filteredJobs;
         }
         
         const firstItem = (this.currentPage - 1) * this.itemsPerPage;
         return this.filteredJobs.slice(firstItem, firstItem + this.itemsPerPage);
      },
      chartSeries: function() {
         return [{
            name: 'Tag count',
            data: this.filteredTags.slice(0, 30).map(t => t.count)
         }] 
      },
      chartOptions: function () {
         return {
            chart: {
               height: 350,
               type: 'bar',
            },
   
            xaxis: {
               categories: this.filteredTags.slice(0, 30).map(t => t.name),
               position: 'bottom',
               axisBorder: {
                  show: false
               },
               axisTicks: {
                  show: false
               },
               crosshairs: {
                  fill: {
                     type: 'gradient',
                     gradient: {
                        colorFrom: '#D8E3F0',
                        colorTo: '#BED1E6',
                        stops: [0, 100],
                        opacityFrom: 0.4,
                        opacityTo: 0.5,
                     }
                  }
               },
               tooltip: {
                  enabled: true,
               }
            },
            yaxis: {
               axisBorder: {
                  show: false
               },
               axisTicks: {
                  show: false,
               }
   
            }
         };
      },
      filteredTags: function () {

         const tags = [];

         for (const job of this.filteredJobs) {
            
            for (const tag of [ ...job.tags, ...job.differentialTags ]) {

               if (!tag) {
                  continue;
               }
               
               let found = false;

               for (const tagObj of tags) {

                  if (tagObj.name == tag) {
                     tagObj.count += 1;
                     found = true;
                     break;
                  }

               }

               if (!found) {
                  tags.push({
                     name: tag,
                     count: 1
                  })
               }

            }

         }

         return tags.sort((a, b) => b.count - a.count);

      },
      totalOfPages: function () {
         return Math.ceil(this.filteredJobs.length / this.itemsPerPage);
      },
      paginationPages: function() {
         
         if (this.totalOfPages >= 10) {
            
            const totalOfPages = this.totalOfPages;
            const currentPage = this.currentPage;
            const pages = [];

            const addPageIfValid = (page) => {
               if (page <= totalOfPages && page >= 1) {
                  pages.push(page);
               }
            }

            if (currentPage - 4 > 0) {
               if (currentPage - 4 == 1) {
                  pages.push(1);
               } else {
                  pages.push(1);
                  pages.push('...');
               }
            }
            
            addPageIfValid(currentPage - 3)
            addPageIfValid(currentPage - 2)
            addPageIfValid(currentPage - 1)

            pages.push(currentPage);

            addPageIfValid(currentPage + 1)
            addPageIfValid(currentPage + 2)
            addPageIfValid(currentPage + 3)
            
            if (currentPage + 4 <= totalOfPages) {
               if (currentPage + 4 == totalOfPages) {
                  pages.push(totalOfPages);
               } else {
                  pages.push('...');
                  pages.push(totalOfPages);
               }
            }
            
            return pages
            
         }

         return Array.from(Array(this.totalOfPages).keys()).map(v => v + 1);
         
      }
   },
   methods: {
      filterRecentJobs: function () {

         const recentJobs = [];
         
         const newJobsSeconds = Math.floor(Date.now() / 1000) - (1 * 24 * 60 * 60)
         
         for (const job of this.jobs) {
            
            if (job.inclusionDate > newJobsSeconds) {
               recentJobs.push(job);
            }
            
         }

         this.recentJobs = recentJobs.reverse();
         
      },
      loadJobs: function () {
         
         axios.get('../data/jobs.json')
            .then(resp => {
               
               let companies = [];
               for (const job of resp.data) {

                  if (!job.differentialTags) {
                     job.differentialTags = [];
                  }

                  job.filters = job.name.toLowerCase() + ' ' + job.tags.join(" ").toLowerCase() + ' ' + job.differentialTags.join(" ").toLowerCase();

                  job.inclusionDateFormat = new Date(job.inclusionDate * 1000).toLocaleString().substring(0, 16);

                  let found = false;

                  for (const comp of companies) {
                     if (comp.name == job.company) {
                        found = true;
                        comp.jobs += 1;
                        break;
                     }
                  }

                  if (!found) {
                     companies.push({
                        name: job.company,
                        jobs: 1
                     });
                  }

               }

               for (const company of companies) {
                  company.nameWithCount = company.name + ' (' + company.jobs + ')';
               }

               this.selectedCompanies = [...companies.filter(c => c.name !== 'TOTVS')];

               this.companies = companies;
               this.jobs = resp.data;
               
               this.filterRecentJobs();
               
            })
            .catch(err => {
               this.error = 'Error loading jobs!';
            })
            .finally(() => {
               this.isLoading = false;
            });

      },
      clearFilters: function () {
         this.selectedCompanies = [];
         this.textFilter = '';
      },
      changeCurrentView: function(view) {
         this.currentView = view;
      }
   }
})
