#!/usr/bin/env ruby
#
# Paginates listings of the `digest` collection (jekyll-paginate only handles
# site.posts). A page or tab opts in with front matter:
#
#   digest_paginate: feed        # a `section` value, or "must_know" for Top Picks
#
# Page 1 renders at the page's own URL; pages 2..N are generated at
# <url>page/N/. Each gets `page.digest_items` (that page's slice, newest first)
# and `page.digest_pager` (consumed by _includes/digest-pager.html).
# Page size comes from `digest_per_page` in _config.yml.

module DigestPaginator
  class Generator < Jekyll::Generator
    safe true
    priority :lowest

    def generate(site)
      digest = site.collections['digest']
      return unless digest

      per_page = (site.config['digest_per_page'] || 25).to_i
      sources = site.pages + site.collections.values.flat_map(&:docs)

      sources.select { |s| s.data['digest_paginate'] }.each do |source|
        filter = source.data['digest_paginate'].to_s
        items = digest.docs.select do |doc|
          filter == 'must_know' ? doc.data['must_know'] == true : doc.data['section'] == filter
        end
        items = items.sort_by(&:date).reverse

        slices = items.each_slice(per_page).to_a
        slices = [[]] if slices.empty?
        base = source.url.end_with?('/') ? source.url : "#{source.url}/"
        page_url = ->(n) { n == 1 ? base : "#{base}page/#{n}/" }

        slices.each_with_index do |slice, i|
          num = i + 1
          target = num == 1 ? source : build_page(site, source, page_url.call(num))
          target.data['digest_items'] = slice
          target.data['digest_pager'] = {
            'page' => num,
            'total_pages' => slices.size,
            'total_items' => items.size,
            'previous_page_path' => num > 1 ? page_url.call(num - 1) : nil,
            'next_page_path' => num < slices.size ? page_url.call(num + 1) : nil,
            'page_paths' => (1..slices.size).map { |n| page_url.call(n) }
          }
        end
      end
    end

    private

    # Clone the source's raw (unrendered) content and front matter into a new
    # page at `url`, so it renders through the same template and layout.
    def build_page(site, source, url)
      page = Jekyll::PageWithoutAFile.new(site, site.source, url, "index#{File.extname(source.path)}")
      page.content = source.content
      page.data = source.data.dup
      page.data['permalink'] = url
      page.data.delete('redirect_from')
      site.pages << page
      page
    end
  end
end
