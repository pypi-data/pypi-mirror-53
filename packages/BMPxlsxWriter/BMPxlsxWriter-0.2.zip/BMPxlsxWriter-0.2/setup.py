from distutils.core import setup
setup(
          name = 'BMPxlsxWriter',
          packages = ['BMPxlsxWriter'],
          version = '0.2',
          license='MIT',
          description = 'The library takes a dictionary of form {Sheet: {Cell: Value}} and updates the specified Excel file accordingly.',
          author = 'Mike Campagna',
          author_email = 'msc94@drexel.edu',
          url = 'https://github.com/mikecampagna',
          download_url = 'https://github.com/TheAcademyofNaturalSciences/BMPxlsxWriter/archive/v_02.tar.gz', # Explain this is a second
          keywords = ['Excel', 'Write', 'XLSX', 'BMP'],
          install_requires=[            # I get to this in a second
                            'openpyxl',
                           ],
          classifiers=[
                       'Development Status :: 5 - Production/Stable',      # Chose "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of package
                       'Intended Audience :: Developers',
                       'Topic :: Software Development :: Build Tools',
                       'License :: OSI Approved :: MIT License',
                       'Programming Language :: Python :: 2.7',
                      ],
)
