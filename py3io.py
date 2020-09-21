# py3io -- python 3 candis io
import sys
import numpy as np

# define the candis class
class candis:

    # initialize the database
    def __init__(self):
        self.comments = []
        self.params = []
        self.dims = []
        self.vfields = []
        self.outlist = []
        self.outstring = ''
        self.vslice = -1
        self.nvslices = 0

    # --------------------------------------------------------------
    # internal methods
    # --------------------------------------------------------------

    # report an error and exit
    def __error(self,message):
        print(message, file=sys.stderr)
        sys.exit(1)

    # check to see if a static field is an index field
    def __indexfld(self,fieldlist):
        if fieldlist[4] == '1':
            if fieldlist[0] == fieldlist[5]:
                return(True)
            else:
                return(False)
        else:
            return(False)

    # compute a field size
    def __fieldsize(self,fieldlist):
        fsize = 0
        dim = int(fieldlist[4])
        if dim >= 0:
            fsize = 1
        if dim >= 1:
            fsize = fsize*int(fieldlist[6])
        if dim >= 2:
            fsize = fsize*int(fieldlist[8])
        if dim >= 3:
            fsize = fsize*int(fieldlist[10])
        if dim >= 4:
            fsize = fsize*int(fieldlist[12])
        return(fsize)

    # unflatten a field
    def __shape(self,flatfld,dimlist):

        # get a list of dimension lengths for field
        ndims = len(dimlist)
        ix = []
        if ndims <= 1:
            return(flatfld)   # nothing to be done for 0 and 1 dims
        else:
            for i in range(len(self.dims)):
                for j in range(ndims):
                    if dimlist[j] == self.dims[i][0]:
                        ix.append(int(self.dims[i][1]))

        # exercise the appropriate reshape
        if ndims == 2:
            return(flatfld.reshape(ix[0],ix[1]))
        elif ndims == 3:
            return(flatfld.reshape(ix[0],ix[1],ix[2]))
        elif ndims == 4:
            return(flatfld.reshape(ix[0],ix[1],ix[2],ix[3]))
        else:
            error('system error: ndims out of range')

    # retrieve the size of a dimension field from the database
    def __dimlength(self,dname):
        for i in range(len(self.dims)):
            dname0 = self.dims[i][0]
            dlen = int(self.dims[i][1])
            if dname0 == dname:
                return(str(dlen))

    # --------------------------------------------------------------
    # input routines -- either a file or standard input (file = '-')
    # --------------------------------------------------------------

    # open a file for output or indicate stdout.buffer is used (False)
    def __openinput(self,infilename):
        if infilename == '-':
            return(False,'')
        else:
            return(True,open(infilename,'rb'))

    # read a chunk of data
    def __readinput(self,handle,nbytes):
        if handle[0]:
            return(handle[1].read(nbytes))
        else:
            return(sys.stdin.buffer.read(nbytes))

    # close output file if not stdout
    def __closeinput(self,handle):
        if handle[0]:
            handle[1].close()

    # get a line from binary input
    def __get_line(self,inhandle):
        linebuffer = b''
        while True:
            charbuffer = self.__readinput(inhandle,1)
            if charbuffer == b'\n':
                return(str(linebuffer.decode('ascii')))
            linebuffer = linebuffer + charbuffer

    # get a slice header from input
    def __get_slice_header(self,inhandle):
        charbuffer = (self.__readinput(inhandle,1)).decode('ascii')
        if (charbuffer != '@') & (charbuffer != ' '):
            return(-1)
        elif charbuffer == '@':
            headerbuffer = (self.__readinput(inhandle,15)).decode('ascii')
        else:
            headerbuffer = (self.__readinput(inhandle,7)).decode('ascii')
            headerbuffer = charbuffer + headerbuffer
        return(int(headerbuffer))

    # --------------------------------------------------------------
    # output routines -- either a file or standard output (file = '-')
    # --------------------------------------------------------------

    # open a file for output or indicate stdout.buffer is used (False)
    def __openoutput(self,outfilename):
        if outfilename == '-':
            return(False,'')
        else:
            return(True,open(outfilename,'wb'))

    # write a chunk of data
    def __writeoutput(self,handle,chunk):
        if handle[0]:
            handle[1].write(chunk)
        else:
            sys.stdout.buffer.write(chunk)

    # close output file if not stdout
    def __closeoutput(self,handle):
        if handle[0]:
            handle[1].close()

    # --------------------------------------------------------------
    # methods to add to the database
    # --------------------------------------------------------------

    # add a comment to the database
    def add_comment(self,comment):
        self.comments.append(comment)
        return(True)

    # add a parameter name-value pair to the database (pval is a string)
    def add_param(self,pname,pval):
        self.params.append([pname, pval])
        return(True)

    # add a dimension to the database -- this is the only type of
    # static field allowed
    def add_dim(self,dname,dsize,ddata):
        self.dims.append([dname, str(dsize), ddata])
        return(True)

    # add a 4-dimensional field to the database -- flatten data if needed
    def add_vfield4(self,fname,dname1,dname2,dname3,dname4,fdata):
        self.vfields.append([fname, '4',
                             dname1, self.__dimlength(dname1),
                             dname2, self.__dimlength(dname2),
                             dname3, self.__dimlength(dname3),
                             dname4, self.__dimlength(dname4),
                             fdata])
        return(True)

    # add a 3-dimensional field to the database -- flatten data if needed
    def add_vfield3(self,fname,dname1,dname2,dname3,fdata):
        self.vfields.append([fname, '3',
                             dname1, self.__dimlength(dname1),
                             dname2, self.__dimlength(dname2),
                             dname3, self.__dimlength(dname3),
                             '', '1',
                             fdata])
        return(True)

    # add a 2-dimensional field to the database -- flatten data if needed
    def add_vfield2(self,fname,dname1,dname2,fdata):
        self.vfields.append([fname, '2',
                             dname1, self.__dimlength(dname1),
                             dname2, self.__dimlength(dname2),
                             '', '1',
                             '', '1',
                             fdata])
        return(True)

    # add a 1-dimensional field to the database
    def add_vfield1(self,fname,dname1,fdata):
        self.vfields.append([fname, '1',
                             dname1, self.__dimlength(dname1),
                             '', '1',
                             '', '1',
                             '', '1',
                             fdata])

        return(True)

    # add a 0-dimensional field to the database -- flattening not needed
    def add_vfield0(self,fname, fdata):
        self.vfields.append([fname, '0',
                             '', '1',
                             '', '1',
                             '', '1',
                             '', '1',
                             fdata])
        return(True)

    # --------------------------------------------------------------
    # methods to examine the database and extract information
    # --------------------------------------------------------------

    # advance to the next variable slice -- returns False if no
    # more slices are available, otherwise True
    def get_next_slice(self):
        if self.vslice < 0:
            error('internal error! vslice < 0')
        elif self.vslice + 1 >= self.nvslices:
            return(False)
        else:
            self.vslice = self.vslice + 1
            return(True)
            
    # get a list of comments
    def get_comment_info(self):
        return(self.comments)

    # get a list of parameter names and values
    def get_param_info(self):
        return(self.params)

    # get the value (string) of a named parameter -- exit on failure
    def get_param(self,pname):
        for i in range(len(self.params)):
            if pname == self.params[i][0]:
                return(self.params[i][1])
        self.__error('parameter "' + pname + '" not found')

    # get dimension information only
    def get_dim_info(self):
        diminfo = []
        for i in range(len(self.dims)):
            diminfo.append([self.dims[i][0],self.dims[i][1]])
        return(diminfo)

    # get variable field information only
    def get_vfield_info(self):
        vfieldinfo = []
        for i in range(len(self.vfields)):
            field = [self.vfields[i][0]]
            for j in range(4):
                next = self.vfields[i][2*j + 2]
                if next != '':
                    field.append(next)
            vfieldinfo.append(field)
        return(vfieldinfo)

    # get named field (dimension or variable field)
    def get_field(self,field):
        for i in range(len(self.dims)):
            if field == self.dims[i][0]:
                return([self.dims[i][2],[self.dims[i][0]]])

        for i in range(len(self.vfields)):
            dimlist = []
            for j in range(4):
                next = self.vfields[i][2*j + 2]
                if next != '':
                    dimlist.append(next)
            if field == self.vfields[i][0]:
                return([self.vfields[i][-1][self.vslice],dimlist])

        self.__error('field "' + field + '" not found')

    # get named field_shaped (dimension or variable field)
    def get_field_shaped(self,field):

        # index fields don't need reshaping
        for i in range(len(self.dims)):
            if field == self.dims[i][0]:
                return([self.dims[i][2],[self.dims[i][0]]])

        # variable fields may need reshaping
        for i in range(len(self.vfields)):
            dimlist = []
            for j in range(4):
                next = self.vfields[i][2*j + 2]
                if next != '':
                    dimlist.append(next)
            if field == self.vfields[i][0]:
                fieldshaped = self.__shape(self.vfields[i][-1][self.vslice],
                                        dimlist)
                return([fieldshaped,dimlist])

        self.__error('field "' + field + '" not found')

    # --------------------------------------------------------------
    # get_candis inputs a candis file, putting the information
    # into the database
    # --------------------------------------------------------------

    def get_candis(self,infilename):

        # open input file if necessary (filename = '-' is stdin)
        inhandle = self.__openinput(infilename)

        # read the header and set up the data base
        tag = 'c'
        checker = 'i'
        while True:
            inputline = self.__get_line(inhandle)

            if (inputline == '***comments***'):
                tag = 'c'
                checker = checker + tag
                if checker != 'ic':
                    __error('header format error')
                    sys.exit(1)

            elif (inputline == '***parameters***'):
                tag = 'p'
                checker = checker + tag
                if checker != 'icp':
                    self.__error('header format error')
                    sys.exit(1)

            elif (inputline == '***static_fields***'):
                tag = 's'
                checker = checker + tag
                if checker != 'icps':
                    self.__error('header format error')
                    sys.exit(1)

            elif (inputline == '***variable_fields***'):
                tag = 'v'
                checker = checker + tag
                if checker != 'icpsv':
                    self.__error('header format error')
                    sys.exit(1)

            elif (inputline == '***format***'):
                tag = 'f'
                checker = checker + tag
                if checker != 'icpsvf':
                    self.__error('header format error')
                    sys.exit(1)

            elif (inputline == 'float'):
                tag = 'g'
                checker = checker + tag
                if checker != 'icpsvfg':
                    self.__error('header format error')
                    sys.exit(1)

            elif (inputline == '*'):
                tag = 'h'
                checker = checker + tag
                if checker != 'icpsvfgh':
                    self.__error('header format error')
                    sys.exit(1)
                break

            elif tag == 'c':
                self.add_comment(inputline)

            elif tag == 'p':

                # in the interests of parameter hygiene, only "bad"
                # and "badlim" transferred -- the 'dim0' and 'ddim'
                # parameters are recreated later from dimension
                # field data
                inputlist = inputline.split()
                pname = inputlist[0]
                pval = inputlist[1]
                if (pname == 'bad') | (pname == 'badlim'):
                    self.add_param(pname,pval)
               
            # the data field temporarily stores a boolean indicating
            # whether this static field is an index field
            elif tag == 's':
                inputlist = inputline.split()
                isindex = self.__indexfld(inputlist)
                dname = inputlist[0]
                dsize = self.__fieldsize(inputlist)
                self.add_dim(dname,dsize,isindex)

            # the field size is stored temporarily in the data field
            elif tag == 'v':
                inputlist = inputline.split()
                fname = inputlist[0]
                dim = int(inputlist[4])
                fsize = self.__fieldsize(inputlist)
                if dim == 4:
                    self.add_vfield4(fname,
                                     inputlist[5],
                                     inputlist[7],
                                     inputlist[9],
                                     inputlist[11],
                                     fsize)

                elif dim == 3:
                    self.add_vfield3(fname,
                                     inputlist[5],
                                     inputlist[7],
                                     inputlist[9],
                                     fsize)

                elif dim == 2:
                    self.add_vfield2(fname,
                                     inputlist[5],
                                     inputlist[7],
                                     fsize)

                elif dim == 1:
                    self.add_vfield1(fname,
                                     inputlist[5],
                                     fsize)

                elif dim == 0:
                    self.add_vfield0(fname,
                                     fsize)

                else:
                    self.__error('field dimension not in range [0-4]')
                    sys.exit(1)

            else:
                self.__error('header format error')
                sys.exit(1)

        # now get static field data, getting rid of non-index fields
        # first check for a match between slice header and static
        # field list
        scount = self.__get_slice_header(inhandle)
        scountdims = 0

        for i in range(len(self.dims)):
            scountdims = scountdims + int(self.dims[i][1])

        if scount != scountdims:
            self.__error('static slice header count inconsistent with data')

        # get the dimension data from the input and eliminate
        # non-index static fields
        self.dims_hold = self.dims
        
        self.dims=[]
        for i in range(len(self.dims_hold)):
            fname = self.dims_hold[i][0]
            size = self.dims_hold[i][1]
            fdata = self.__readinput(inhandle,4*int(size))
            if self.dims_hold[i][2]:
                if sys.byteorder == 'big':
                    self.dims.append([fname,size,
                                      np.fromstring(fdata,dtype='float32',
                                                    count=int(size),sep='')])
                else:
                    self.dims.append([fname,size,
                                      np.fromstring(fdata,dtype='float32',
                                                    count=int(size),sep='')
                                      .byteswap()])

        # add default bad and badlim parameters if these don't exist
        # in an input file
        nogotbad = True
        for i in range(len(self.params)):
            if (self.params[i][0] == 'bad') or (self.params[i][0] == 'badlim'):
                nogotbad = False
        if nogotbad:
            self.add_param('bad','1.e30')
            self.add_param('badlim','9.99e29')

        # OK, now let's do the variable slices
        # compute variable slice size from database
        vcountdims = 0
        vfsizelist = []
        for i in range(len(self.vfields)):
            vfsize = int(self.vfields[i][-1])
            vfsizelist.append(vfsize)
            vcountdims = vcountdims + vfsize

            # assign an empty list to the data field now that we have
            # extracted the field size
            self.vfields[i][-1] = []

        # loop on input to read in the variable slices one by one
        self.nvslices = 0
        while (1):

            # get the slice size from the slice header and compare to
            # database-derived size
            vcount = self.__get_slice_header(inhandle)

            # break out of loop if out of variable slices
            if vcount < 0:
                break

            # check that new slice is of the correct size
            if vcountdims != vcount:
                self.__error(
                    'variable slice header count inconsistent with data')

            # loop through fields and extract data
            for i in range(len(self.vfields)):
                vsize = vfsizelist[i]
                fdata = self.__readinput(inhandle,4*vsize)
                if sys.byteorder == 'big':
                    rawfld = np.fromstring(fdata,dtype='float32',
                                           count=vsize,sep='')
                else:
                    rawfld = np.fromstring(fdata,dtype='float32',
                                           count=vsize,sep='').byteswap()

                # flatten input field if needed
                self.vfields[i][-1].append(rawfld.reshape(np.size(rawfld)))

            # increment the number of variable slices
            self.nvslices = self.nvslices + 1

        # close input file if necessary
        self.__closeinput(inhandle)

        # set to the first variable slice
        self.vslice = 0

        return(True)

    # --------------------------------------------------------------
    # put_candis outputs a candis file, taking the information
    # from the database
    # --------------------------------------------------------------

    def put_candis(self,outfilename):

        # get a file handle for output
        outhandle = self.__openoutput(outfilename)

        # create a list of strings to concatenated as the candis header
        # comment section
        self.outlist.append('***comments***')
        for i in range(len(self.comments)):
            self.outlist.append(self.comments[i])

        # parameters section -- check for pre-existing bad/badlim
        self.outlist.append('***parameters***')
        nogotbad = True
        for i in range(len(self.params)):
            if (self.params[i][0] == 'bad') | (self.params[i][0] == 'badlim'):
                nogotbad = False
            self.outlist.append(self.params[i][0] + ' ' + self.params[i][1])

        # if no bad/badlim in parameter list, put in default values
        if nogotbad:
            self.outlist.append('bad 1.e30')
            self.outlist.append('badlim 9.99e29')

        # recreate parameters for index fields (some programs
        # still need these!) assumes equally spaced data
        for i in range(len(self.dims)):
            dname = self.dims[i][0]
            x0 = self.dims[i][2][0]
            dx = self.dims[i][2][1] - x0
            self.outlist.append(dname + '0 ' + str(x0))
            self.outlist.append('d' + dname + ' ' + str(dx))

        # now add the static field stuff
        self.outlist.append('***static_fields***')
        for i in range(len(self.dims)):
            dname = self.dims[i][0]
            self.outlist.append(dname
                                + ' 1 0 l 1'
                                + ' ' + self.dims[i][0]
                                + ' ' + self.dims[i][1])

        # variable fields section
        self.outlist.append('***variable_fields***')
        for i in range(len(self.vfields)):
            fielddim = self.vfields[i][1]

            if fielddim == str(0):
                self.outlist.append(self.vfields[i][0] + ' 1 0 l 0')

            if fielddim == str(1):
                self.outlist.append(self.vfields[i][0] + ' 1 0 l 1'
                                    + ' ' + self.vfields[i][2]
                                    + ' ' + self.vfields[i][3])

            if fielddim == str(2):
                self.outlist.append(self.vfields[i][0] + ' 1 0 l 2'
                                    + ' ' + self.vfields[i][2]
                                    + ' ' + self.vfields[i][3]
                                    + ' ' + self.vfields[i][4]
                                    + ' ' + self.vfields[i][5])

            if fielddim == str(3):
                self.outlist.append(self.vfields[i][0] + ' 1 0 l 3'
                                    + ' ' + self.vfields[i][2]
                                    + ' ' + self.vfields[i][3]
                                    + ' ' + self.vfields[i][4]
                                    + ' ' + self.vfields[i][5]
                                    + ' ' + self.vfields[i][6]
                                    + ' ' + self.vfields[i][7])

            if fielddim == str(4):
                self.outlist.append(self.vfields[i][0] + ' 1 0 l 4'
                                    + ' ' + self.vfields[i][2]
                                    + ' ' + self.vfields[i][3]
                                    + ' ' + self.vfields[i][4]
                                    + ' ' + self.vfields[i][5]
                                    + ' ' + self.vfields[i][6]
                                    + ' ' + self.vfields[i][7]
                                    + ' ' + self.vfields[i][8]
                                    + ' ' + self.vfields[i][9])

        # stuff at the end of the candis header -- float format only
        self.outlist.append('***format***\nfloat\n*')

        # cat all the strings together separated by newlines
        for i in range(len(self.outlist)):
            self.outstring = self.outstring + self.outlist[i] + '\n'

        # send the assembled header to standard output
        self.__writeoutput(outhandle,bytes(self.outstring, 'ascii'))

        # compute static element count and print
        scount = 0
        for i in range(len(self.dims)):
            scount = scount + int(self.dims[i][1])
        self.__writeoutput(outhandle,
                           bytes("@" + repr(scount).rjust(15), 'ascii'))

        # print each static slice -- native candis endianness is 'big'
        if sys.byteorder == 'big':
            for i in range(len(self.dims)):
                self.__writeoutput(outhandle,
                    self.dims[i][2].astype('float32'))   
        else:
            for i in range(len(self.dims)):
                self.__writeoutput(outhandle,
                    self.dims[i][2].astype('float32').byteswap())
            
        # compute variable element count
        # also test for zero variable fields and inconsistent
        # numbers of slices between variable fields
        vcount = 0
        vsizelist = []
        numv = 0
        nfields = 0

        for i in range(len(self.vfields)):
            dsize1 = int(self.vfields[i][3])
            dsize2 = int(self.vfields[i][5])
            dsize3 = int(self.vfields[i][7])
            dsize4 = int(self.vfields[i][9])

            vsize = dsize1*dsize2*dsize3*dsize4
            vcount = vcount + vsize
            vsizelist.append(vsize)
            numvold = numv
            numv = len(self.vfields[i][10])

            if numv == 0:
                self.__error('a variable field has zero variable slices')

            if i > 0:
                if numv != numvold:
                    self.__error(
                        'variable fields have different numbers of slices')

            nfields = nfields + 1

        if nfields == 0:
            self.__error('no variable fields')

        # loop over variable slices
        for i in range(numv):

            # print word count for each variable slice
            self.__writeoutput(outhandle,bytes("@" + repr(vcount).rjust(15),
                                               'ascii'))


            # print each variable slice -- native candis endianness is 'big'
            if sys.byteorder == 'big':
                for j in range(nfields):
                    self.__writeoutput(outhandle,
                        self.vfields[j][10][i].astype('float32'))   
            else:
                for j in range(nfields):
                    self.__writeoutput(outhandle,
                        self.vfields[j][10][i].astype('float32').byteswap())

        # close the output file if necessary
        self.__closeoutput(outhandle)
        return(True)
