
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
      textFilter: '',
      currentPage: 1,
      totalOfPages: 0,
      itemsPerPage: 10
   },
   mounted: function () {
      this.loadJobs();
   },
   computed: {
      filteredJobs: function () {
         
         if (this.isLoading) {
            return [];
         }
         
         const companyNames = this.selectedCompanies.map(company => company.name);

         return this.jobs.filter(job => {
            return companyNames.includes(job.company) && (!this.textFilter || job.filters.includes(this.textFilter.toLowerCase()));
         });
      },
      paggedJobs: function () {
         return this.filteredJobs.slice((this.currentPage - 1) * this.itemsPerPage, this.currentPage * this.itemsPerPage);
      },
      chartSeries: function() {
         return [{
            name: 'Tag count',
            data: this.filteredTags.slice(0, 30).map(t => t.count) // [2.3, 3.1, 4.0, 10.1, 4.0, 3.6, 3.2, 2.3, 1.4, 0.8, 0.5, 0.2]
         }] 
      },
      chartOptions: function () {
         return {
            chart: {
               height: 350,
               type: 'bar',
            },
   
            xaxis: {
               categories: this.filteredTags.slice(0, 30).map(t => t.name), // ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
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

      }
   },
   methods: {
      loadJobs: function () {

         axios.get('../data/jobs.json')
            .then(resp => {

               let companies = [];
               for (const job of resp.data) {

                  if (!job.differentialTags) {
                     job.differentialTags = [];
                  }

                  job.filters = job.name.toLowerCase() + ' ' + job.tags.join(" ").toLowerCase() + ' ' + job.differentialTags.join(" ").toLowerCase();

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
               
               this.totalOfPages = Math.ceil(this.jobs.length / this.itemsPerPage);

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
      }
   }
})
